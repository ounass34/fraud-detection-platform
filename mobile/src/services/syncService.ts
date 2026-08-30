import NetInfo from "@react-native-community/netinfo";
import {db} from "../db/database";
const API=process.env.EXPO_PUBLIC_API_URL||"http://localhost:8000/api/v1";
export async function syncPendingInspections(){const n=await NetInfo.fetch();if(!n.isConnected)return;const rows=db.getAllSync<{id:string,payload:string}>("SELECT id,payload FROM inspection_queue");for(const x of rows){try{const r=await fetch(`${API}/inspections/submit`,{method:"POST",headers:{"Content-Type":"application/json"},body:x.payload});if(r.ok)db.runSync("DELETE FROM inspection_queue WHERE id=?",[x.id])}catch(e){console.warn("Sync failed",e)}}}
export function watchNetwork(){return NetInfo.addEventListener(s=>{if(s.isConnected)syncPendingInspections()})}
