import {useState} from "react";
import FraudMap from "./components/FraudMap";
import SuspectList from "./components/SuspectList";
import ClientDiagnostic from "./components/ClientDiagnostic";
export default function App(){
 const [view,setView]=useState("map");
 return <div className="h-full bg-slate-100"><header className="h-14 bg-slate-900 text-white flex items-center px-5 gap-6"><b>PNT Fraud Detection</b><button onClick={()=>setView("map")}>Carte</button><button onClick={()=>setView("suspects")}>Suspects</button><button onClick={()=>setView("diagnostic")}>Diagnostic IA</button></header><main className="h-[calc(100%-3.5rem)]">{view==="map"&&<FraudMap/>}{view==="suspects"&&<SuspectList/>}{view==="diagnostic"&&<ClientDiagnostic/>}</main></div>
}
