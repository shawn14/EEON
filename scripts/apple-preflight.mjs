// Read-only EEON release inventory, using the established Milepost ASC client.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const file = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(file), '..');
const fastlaneRoot = path.resolve(root, '../fastlane-configs');
const config = fs.readFileSync(path.join(fastlaneRoot, 'fastlane/Fastfile'), 'utf8');
const appConfig = config.split("'voice-notes' => {")[1]?.split("\n  },")[0];
const bundle = appConfig?.match(/bundle_id: '([^']+)'/)?.[1];
const appId = appConfig?.match(/apple_id: '([^']+)'/)?.[1];
if (!bundle || !appId) throw new Error('EEON identity missing from canonical Fastfile');
export default async function preflight(api) {
  const sources = [];
  async function read(url) { sources.push(url); return api.get(url); }
  const app = (await read(`/v1/apps/${appId}`)).data;
  if (app.attributes.bundleId !== bundle) throw new Error('Apple app identity differs from Fastfile');
  const versions = (await read(`/v1/apps/${appId}/appStoreVersions?filter[platform]=IOS&limit=50`)).data;
  const builds = await read(`/v1/builds?filter[app]=${appId}&sort=-uploadedDate&limit=10&include=preReleaseVersion,buildBetaDetail`);
  const reviews = (await read(`/v1/apps/${appId}/reviewSubmissions?limit=50`)).data;
  const subscriptions = [];
  for (const group of (await read(`/v1/apps/${appId}/subscriptionGroups?limit=50`)).data) {
    for (const sub of (await read(`/v1/subscriptionGroups/${group.id}/subscriptions?limit=50`)).data) {
      subscriptions.push({id:sub.id,productId:sub.attributes.productId,state:sub.attributes.state});
    }
  }
  const schedule = (await read(`/v1/apps/${appId}/appPriceSchedule`)).data;
  const downloadPrices = [];
  for (const kind of ['manualPrices','automaticPrices']) {
    let url=`/v1/appPriceSchedules/${schedule.id}/${kind}?include=appPricePoint,territory&limit=200`;
    while (url) {
      const page=await read(url);
      for (const price of page.data) {
        const point=page.included.find(p=>p.type==='appPricePoints' && p.id===price.relationships.appPricePoint.data.id);
        if (!point || !Number.isFinite(Number(point.attributes.customerPrice))) throw new Error('Missing actual app download price');
        downloadPrices.push({territory:price.relationships.territory.data.id,price:Number(point.attributes.customerPrice),startDate:price.attributes.startDate,endDate:price.attributes.endDate});
      }
      url=page.links?.next;
    }
  }
  if (!downloadPrices.length || downloadPrices.some(p=>p.price!==0)) throw new Error('Download is not verified Free');
  const active = [];
  for (const v of versions.filter(v => ['PREPARE_FOR_SUBMISSION','WAITING_FOR_REVIEW','IN_REVIEW','PENDING_DEVELOPER_RELEASE','READY_FOR_SALE','READY_FOR_DISTRIBUTION','DEVELOPER_REJECTED','REJECTED'].includes(v.attributes.appStoreState)).slice(0,4)) {
    const build = (await read(`/v1/appStoreVersions/${v.id}/build`)).data;
    active.push({id:v.id,version:v.attributes.versionString,state:v.attributes.appStoreState,releaseType:v.attributes.releaseType,build:build ? {id:build.id,number:build.attributes.version}:null});
  }
  // Preserve the exact existing phone/tablet/Watch assets on this bug-fix release.
  const project=fs.readFileSync(path.join(root,'voice notes.xcodeproj/project.pbxproj'),'utf8');
  const targetVersion=project.match(/MARKETING_VERSION = ([^;]+);/)[1];
  const live=versions.filter(v=>['READY_FOR_SALE','READY_FOR_DISTRIBUTION'].includes(v.attributes.appStoreState))
    .sort((a,b)=>b.attributes.versionString.localeCompare(a.attributes.versionString,undefined,{numeric:true}))[0];
  const listingAssets=[];
  for(const v of versions.filter(v=>v.attributes.versionString===targetVersion || v.id===live?.id)) {
    const locales=(await read(`/v1/appStoreVersions/${v.id}/appStoreVersionLocalizations?limit=50`)).data;
    for(const locale of locales) {
      const sets=(await read(`/v1/appStoreVersionLocalizations/${locale.id}/appScreenshotSets?limit=50`)).data;
      const screenshots=[];
      for(const set of sets) {
        const images=(await read(`/v1/appScreenshotSets/${set.id}/appScreenshots?limit=50`)).data;
        for(const image of images) screenshots.push({displayType:set.attributes.screenshotDisplayType,fileName:image.attributes.fileName,checksum:image.attributes.sourceFileChecksum,state:image.attributes.assetDeliveryState?.state});
      }
      listingAssets.push({version:v.attributes.versionString,locale:locale.attributes.locale,whatsNew:locale.attributes.whatsNew,screenshots});
    }
  }
  return {observedAt:new Date().toISOString(),readOnly:true,appId,bundle,source:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),fastlaneSource:execFileSync('git',['rev-parse','HEAD'],{cwd:fastlaneRoot,encoding:'utf8'}).trim(),versions:versions.map(v=>({id:v.id,version:v.attributes.versionString,state:v.attributes.appStoreState,releaseType:v.attributes.releaseType})),active,builds:builds.data.map(b=>({id:b.id,...b.attributes,relationships:b.relationships})),included:builds.included,reviews:reviews.map(r=>({id:r.id,...r.attributes})),subscriptions,downloadPrices,listingAssets,sources};
}
if (process.argv[1] && path.resolve(process.argv[1]) === file) {
  const client = path.resolve(root,'../milepost/scripts/asc/asc.mjs');
  if (!fs.existsSync(client)) throw new Error('Canonical ASC client is unavailable');
  const output=file.replace(/\.mjs$/,'.out.json');
  const started=Date.now();
  const run=spawnSync(process.execPath,[client,file],{cwd:root,stdio:'inherit',timeout:120000});
  if(run.error || run.status!==0) throw run.error || new Error(`ASC client exit ${run.status}`);
  if(!fs.existsSync(output) || fs.statSync(output).mtimeMs < started-1000) throw new Error('Fresh ASC receipt missing');
  const receipt=JSON.parse(fs.readFileSync(output,'utf8'));
  const dest=path.join(root,'build/apple-release'); fs.mkdirSync(dest,{recursive:true});
  const saved=path.join(dest,`apple-${Date.now()}.json`); fs.renameSync(output,saved);
  if(!receipt.ok) throw new Error(receipt.error || 'ASC read failed');
  console.log(JSON.stringify(receipt.result,null,2)); console.log(`Receipt: ${saved}`);
}
