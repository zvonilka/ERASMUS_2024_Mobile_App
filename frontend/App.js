import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, Text, TouchableOpacity, TextInput, Alert, ScrollView, Keyboard, TouchableWithoutFeedback } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import ImageViewer from './components/ImageViewer'; // This will show an image

const PlaceholderImage = require('./assets/logo.png'); // loads an image
const Stack = createStackNavigator(); // creates screen navigation

// Custom Buttons creater
function Button({ label, onPress }) {
  return (
    <TouchableOpacity style={styles.button} onPress={onPress}>
      <Text style={styles.buttonLabel}>{label}</Text>
    </TouchableOpacity>
  );
}

// home Screen with button that navigates to Dashboard
function HomeScreen({ navigation }) {
  const handleDashboardPress = () => {
    navigation.navigate('Dashboard');
  };

  return (
    <View style={styles.container}>
      <View style={styles.imageContainer}>
        <ImageViewer placeholderImageSource={PlaceholderImage} />
      </View>
      <View style={styles.footerContainer}>
        <Button label="Start Chatting!" onPress={handleDashboardPress} />
      </View>
      <StatusBar style="auto" />
    </View>
  );
}

// chats interfec
function DashboardScreen() {
  const [ws, setWs] = useState(null);
  const [messages, setMessages] = useState([]);
  const [sendMessage, setSendMessage] = useState('');

  useEffect(() => {
    const webSocket = new WebSocket('ws://192.168.214.11:8000'); // your local server IP for server

    webSocket.onopen = () => {
      console.log('Connected to the server');
      setWs(webSocket);
    };

    webSocket.onmessage = (message) => {
      console.log(`Received: ${message.data}`);
      setMessages(prevMessages => [...prevMessages, message.data]); // add received message
    };

    webSocket.onerror = (error) => {
      console.error(`WebSocket error: ${error.message}`);
    };

    webSocket.onclose = () => {
      console.log('Disconnected from server');
    };

    return () => {
      webSocket.close();
    };
  }, []);

  const handleSendMessage = () => {
    if (ws && sendMessage) {
      ws.send(`${sendMessage}`); // send message
    } else {
      Alert.alert('Error', 'WebSocket is not connected or message is empty');
    }
  };

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        <Text style={styles.tex}>Enter the message:</Text>
        <TextInput
          style={styles.input}
          placeholder="Message"
          value={sendMessage}
          onChangeText={setSendMessage}
        />
        <Button label="Send Message" onPress={handleSendMessage} />
        <Text style={styles.tex}>Messages:</Text>
        <ScrollView style={styles.scrollContainer}>
          {messages.map((msg, index) => (
            <Text style={styles.tex} key={index}>{msg}</Text>
          ))}
        </ScrollView>
      </View>
    </TouchableWithoutFeedback>
  );
}

// first screen with navigation setup
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#25292e',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  input: {
    width: 200,
    padding: 10,
    height: 40,
    backgroundColor: '#333',
    color: '#fff',
    paddingHorizontal: 10,
    borderRadius: 5,
    marginBottom: 20,
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#f3f3f3',
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderRadius: 5,
    marginTop: 10,
  },
  buttonLabel: {
    color: '#0f0f0f',
    fontSize: 16,
    fontWeight: 'bold',
  },
  tex: {
    color: '#f3f3f3',
  },
  scrollContainer: {
    width: 240,
    maxHeight: 300,
  },
  imageContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  footerContainer: {
    flex: 1,
  }
});
