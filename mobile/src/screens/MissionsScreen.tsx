import {useEffect,useState} from "react";
import {View,Text,FlatList,Button} from "react-native";
import * as Location from "expo-location";
import {db} from "../db/database";
import {distanceKm} from "../services/locationService";
import {syncPendingInspections} from "../services/syncService";
type M={id:string,customer_name:string,latitude:number,longitude:number,risk_score:number};
export default function MissionsScreen(){const [missions,setMissions]=useState<M[]>([]);async function load(){const p=await Location.requestForegroundPermissionsAsync();const rows=db.getAllSync<M>("SELECT id,customer_name,latitude,longitude,risk_score FROM missions");if(p.status!=="granted")return setMissions(rows);const pos=await Location.getCurrentPositionAsync({});setMissions([...rows].sort((a,b)=>distanceKm(pos.coords.latitude,pos.coords.longitude,a.latitude,a.longitude)-distanceKm(pos.coords.latitude,pos.coords.longitude,b.latitude,b.longitude)))}useEffect(()=>{load()},[]);return <View style={{flex:1,padding:16}}><Button title="Synchroniser" onPress={syncPendingInspections}/><FlatList data={missions} keyExtractor={x=>x.id} renderItem={({item})=><View style={{padding:12,borderBottomWidth:1}}><Text>{item.customer_name}</Text><Text>Risque: {item.risk_score}%</Text></View>} ListEmptyComponent={<Text>Aucune mission locale.</Text>}/></View>}
