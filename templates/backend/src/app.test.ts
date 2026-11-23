import assert from 'node:assert/strict';
import { after, before, test } from 'node:test';
import { createServer, type Server } from 'node:http';
import { createApp } from './app.js';
let server:Server;
let url:string;
before(async()=>{
  server=createServer(createApp('https://example.test'));
  await new Promise<void>((resolve)=>server.listen(0,'127.0.0.1',resolve));
  const address=server.address();
  if(!address || typeof address==='string')throw new Error('Missing test port');
  url=`http://127.0.0.1:${address.port}`;
});
after(()=>new Promise<void>((resolve,reject)=>server.close(err=>err?reject(err):resolve())));
test('health returns ready status',async()=>{const r=await fetch(url+'/health');assert.equal(r.status,200);assert.deepEqual(await r.json(),{status:'ok'});});
test('input validation blocks unknown properties',async()=>{const r=await fetch(url+'/api/notes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:'hi',unexpected:true})});assert.equal(r.status,400);});
test('note creation and listing',async()=>{const r=await fetch(url+'/api/notes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:'test message'})});assert.equal(r.status,201);const item=await r.json();assert.equal(item.message,'test message');const listed=await (await fetch(url+'/api/notes')).json();assert.ok(listed.items.some((x:{id:string})=>x.id===item.id));});
test('CORS only allows configured origin',async()=>{const good=await fetch(url+'/health',{headers:{Origin:'https://example.test'}});assert.equal(good.headers.get('access-control-allow-origin'),'https://example.test');const bad=await fetch(url+'/health',{headers:{Origin:'https://evil.test'}});assert.equal(bad.headers.get('access-control-allow-origin'),null);});
