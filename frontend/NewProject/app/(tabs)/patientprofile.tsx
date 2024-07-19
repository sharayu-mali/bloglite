import Constants from 'expo-constants';
import { ScrollViewStyleReset } from 'expo-router/html';
import React, { useState } from 'react';
import { StyleSheet, Text, TextInput, View , Button, Alert, ScrollView, Switch,Image} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import Icons from 'react-native-vector-icons/Ionicons';
import { isEnabled } from 'react-native/Libraries/Performance/Systrace';
import Patientsettings from '@/components/Patientsettings';

 export const patientprofile = () => {
  const [username, setUsername] = useState  ('');
  const [isEnabled, toggleSwitch] = useState(false);


    //  function toggleSwitch(value: boolean): void | Promise<void> {
    //     //  throw new Error('Function not implemented.');
    //  }

  return (

    <View>
    {/* <Text>dkfjbgkj</Text>
        <Image
            source={require('../../assets/images/patient.jpg')}
            
        /> */}
    <Patientsettings/>

    </View>
  );
};

export default patientprofile;
