import {useState} from "react";
import {ResponsiveContainer,LineChart,Line,XAxis,YAxis,Tooltip,BarChart,Bar} from "recharts";
const load=[{time:"00h",customer:1.2,peer:2.1},{time:"06h",customer:1.5,peer:2.8},{time:"12h",customer:2.2,peer:4.0},{time:"18h",customer:1.8,peer:4.5}];
const demo=[{feature:"Peer ratio",shap_value:.31},{feature:"Historical drop",shap_value:.22},{feature:"Night load",shap_value:.15}];
export default function ClientDiagnostic(){
 const [id,setId]=useState(""),[exp,setExp]=useState(null);
 async function analyse(){if(id){const r=await fetch(`/api/v1/fraud/suspects/${id}/explain`);setExp(await r.json());}}
 const shap=exp?.top_factors?.length?exp.top_factors:demo;
 return <div className="p-6 space-y-6"><div className="flex gap-2"><input className="border p-2 flex-1" placeholder="UUID client" value={id} onChange={e=>setId(e.target.value)}/><button className="bg-slate-800 text-white px-4" onClick={analyse}>Analyser</button></div><section className="bg-white p-5"><h2>Courbe de charge vs groupe pair</h2><ResponsiveContainer width="100%" height={280}><LineChart data={load}><XAxis dataKey="time"/><YAxis/><Tooltip/><Line dataKey="customer"/><Line dataKey="peer"/></LineChart></ResponsiveContainer></section><section className="bg-white p-5"><h2>Explication SHAP</h2><ResponsiveContainer width="100%" height={280}><BarChart data={shap} layout="vertical"><XAxis type="number"/><YAxis type="category" dataKey="feature"/><Tooltip/><Bar dataKey="shap_value"/></BarChart></ResponsiveContainer></section></div>
}
