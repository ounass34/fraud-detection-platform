import {useEffect,useState} from "react";
import {MapContainer,TileLayer,CircleMarker,Popup} from "react-leaflet";
import "leaflet/dist/leaflet.css";
const color=s=>s>80?"#ef4444":s>=50?"#f97316":"#22c55e";
export default function FraudMap(){
 const [data,setData]=useState([]);
 useEffect(()=>{fetch("/api/v1/fraud/suspects").then(r=>r.json()).then(x=>setData(x.data||[]));},[]);
 return <MapContainer center={[4.05,9.70]} zoom={12} className="h-full w-full"><TileLayer attribution="© OpenStreetMap" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>{data.filter(x=>x.latitude!=null&&x.longitude!=null).map(c=><CircleMarker key={c.customer_id} center={[c.latitude,c.longitude]} radius={8} pathOptions={{color:color(c.risk_score),fillOpacity:.8}}><Popup><b>{c.full_name||c.account_number}</b><br/>Score: {c.risk_score}%<br/>Perte: {c.estimated_loss_kwh??0} kWh</Popup></CircleMarker>)}</MapContainer>
}
