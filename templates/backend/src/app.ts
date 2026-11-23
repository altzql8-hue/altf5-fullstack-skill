import express, { type ErrorRequestHandler } from 'express';
import { z } from 'zod';
import { randomUUID } from 'node:crypto';

const messageSchema = z.object({ message: z.string().trim().min(1).max(280) }).strict();
const records = new Map<string,{ id:string, message:string }>();

export function createApp(allowedOrigin = process.env.CORS_ORIGIN ?? 'http://localhost:5173') {
  const app = express();
  app.disable('x-powered-by');
  app.use((_req,res,next)=>{res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','no-referrer');res.setHeader('X-Frame-Options','DENY');next();});
  app.use((req,res,next)=>{
    const origin = req.get('Origin');
    if(origin && origin === allowedOrigin){res.setHeader('Access-Control-Allow-Origin',allowedOrigin);res.setHeader('Vary','Origin');res.setHeader('Access-Control-Allow-Methods','GET, POST, OPTIONS');res.setHeader('Access-Control-Allow-Headers','Content-Type');}
    if(req.method === 'OPTIONS')return res.sendStatus(origin && origin === allowedOrigin?204:403);
    next();
  });
  app.use(express.json({limit:'8kb'}));
  app.get('/health',(_req,res)=>res.json({status:'ok'}));
  app.get('/api/notes',(_req,res)=>res.json({items:[...records.values()]}));
  app.post('/api/notes',(req,res)=>{
    const parsed=messageSchema.safeParse(req.body);
    if(!parsed.success)return res.status(400).json({error:'invalid_request',details:parsed.error.issues.map(e=>({path:e.path.join('.'),message:e.message}))});
    const item={id:randomUUID(),message:parsed.data.message};
    records.set(item.id,item);
    return res.status(201).json(item);
  });
  const onError:ErrorRequestHandler=(err,_req,res,_next)=>{
    if(err instanceof SyntaxError && 'body' in err)return res.status(400).json({error:'invalid_json'});
    if(err?.type==='entity.too.large')return res.status(413).json({error:'payload_too_large'});
    console.error('Unhandled request failure',err);
    return res.status(500).json({error:'internal_error'});
  };
  app.use(onError);
  return app;
}
