import {useState} from "react";
import {View,Text,Button,Alert} from "react-native";
import * as Location from "expo-location";
import {queueInspection} from "../db/database";
const types=["BYPASS","VOLTAGE_TAMPERING","CURRENT_TRANSFORMER_SHUNT","METER_STOPPED","NONE"];
export default function InspectionScreen({inspectionId}:{inspectionId:string}){const [type,setType]=useState("NONE");async function submit(){const l=await Location.getCurrentPositionAsync({});queueInspection(inspectionId,{inspection_id:inspectionId,fraud_confirmed:type!=="NONE",fraud_type:type,latitude:l.coords.latitude,longitude:l.coords.longitude,gps_accuracy_m:l.coords.accuracy,device_id:"DEVICE_ID_TO_IMPLEMENT",completed_at:new Date().toISOString(),evidence:[]});Alert.alert("Inspection enregistrée hors-ligne")}return <View style={{padding:16,gap:10}}><Text>Type de fraude</Text>{types.map(x=><Button key={x} title={x} onPress={()=>setType(x)}/>)}<Button title="Valider hors-ligne" onPress={submit}/></View>}
