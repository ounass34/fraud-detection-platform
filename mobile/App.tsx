import {useEffect} from "react";
import {SafeAreaView} from "react-native";
import {initializeDatabase} from "./src/db/database";
import {watchNetwork} from "./src/services/syncService";
import MissionsScreen from "./src/screens/MissionsScreen";
export default function App(){useEffect(()=>{initializeDatabase();const u=watchNetwork();return()=>u();},[]);return <SafeAreaView style={{flex:1}}><MissionsScreen/></SafeAreaView>}
