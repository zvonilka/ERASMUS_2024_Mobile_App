import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, View, Text, TouchableOpacity, TextInput, Alert, FlatList } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import ImageViewer from './components/ImageViewer'; // Assuming it's set up correctly

const PlaceholderImage = require('./assets/logo.png');
const Stack = createStackNavigator();

// Dummy user data
const users = [
  { id: '1', name: 'Alice' },
  { id: '2', name: 'Bob' },
  { id: '3', name: 'Charlie' },
];

const messagesData = {
  '1': [{ id: '1', text: 'Hello Alice!' }, { id: '2', text: 'How are you?' }],
  '2': [{ id: '1', text: 'Hey Bob!' }, { id: '2', text: 'Let’s chat!' }],
  '3': [{ id: '1', text: 'Hi Charlie!' }, { id: '2', text: 'What’s up?' }],
};

// Custom Button Component
function Button({ label, onPress }) {
  return (
    <TouchableOpacity style={styles.button} onPress={onPress}>
      <Text style={styles.buttonLabel}>{label}</Text>
    </TouchableOpacity>
  );
}

function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <View style={styles.imageContainer}>
        <ImageViewer placeholderImageSource={PlaceholderImage} />
      </View>
      <View style={styles.footerContainer}>
        <Button label="LOGIN" onPress={() => navigation.navigate('Login')} />
        <Button label="SIGN UP" onPress={() => navigation.navigate('Signup')} />
      </View>
      <StatusBar style="auto" />
    </View>
  );
}

function LoginScreen({ navigation }) {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    console.log("Login submitted with:", { name, password });
    if (name === 'admin' && password === 'admin') {
      navigation.navigate('Dashboard');
    } else {
      Alert.alert('Invalid credentials', 'Please enter valid username and password.');
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter Name"
        placeholderTextColor="#aaa"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter Password"
        placeholderTextColor="#aaa"
        secureTextEntry={true}
        value={password}
        onChangeText={setPassword}
      />
      <Button label="LOGIN" onPress={handleSubmit} />
    </View>
  );
}

function SignupScreen() {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    console.log("Signup submitted with:", { name, password });
    /* Placeholder for signup logic */
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter Name"
        placeholderTextColor="#aaa"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter Password"
        placeholderTextColor="#aaa"
        secureTextEntry={true}
        value={password}
        onChangeText={setPassword}
      />
      <Button label="SIGN UP" onPress={handleSubmit} />
    </View>
  );
}

function ChatScreen({ route, navigation }) {
  const { user } = route.params;
  const [message, setMessage] = useState('');
  const messages = messagesData[user.id] || [];

  const handleSend = () => {
    if (message) {
      messages.push({ id: `${messages.length + 1}`, text: message });
      setMessage('');
      Alert.alert('Message Sent', `Your message to ${user.name}: "${message}"`); // Simulating sending a message
    } else {
      Alert.alert('Error', 'Please enter a message.');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.chatHeader}>{`Chat with ${user.name}`}</Text>
      <FlatList
        data={messages}
        renderItem={({ item }) => <Text style={styles.message}>{item.text}</Text>}
        keyExtractor={item => item.id}
        style={styles.messageList}
      />
      <TextInput
        style={styles.input}
        placeholder="Type a message"
        placeholderTextColor="#aaa"
        value={message}
        onChangeText={setMessage}
      />
      <Button label="SEND" onPress={handleSend} />
      <Button label="BACK" onPress={() => navigation.goBack()} />
    </View>
  );
}

function DashboardScreen({ navigation }) {
  const [isVisible, setIsVisible] = useState(false);
  const [userIP] = useState('192.168.1.1');

  const toggleTextVisibility = () => {
    setIsVisible(!isVisible);
  };

  const handleUserPress = (user) => {
    navigation.navigate('Chat', { user });
  };

  const renderUser = ({ item }) => (
    <TouchableOpacity style={styles.userContainer} onPress={() => handleUserPress(item)}>
      <Text style={styles.userName}>{item.name}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={toggleTextVisibility} style={styles.censoredContainer}>
        <Text style={styles.censoredText}>
          {isVisible ? `Your IP: ${userIP}` : "Show IP"}
        </Text>
      </TouchableOpacity>
      <FlatList
        data={users}
        renderItem={renderUser}
        keyExtractor={item => item.id}
        style={styles.userList}
      />
    </View>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Signup" component={SignupScreen} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
        <Stack.Screen name="Chat" component={ChatScreen} />
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
  imageContainer: {
    flex: 1 / 3,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 250,
    paddingBottom: 60,
  },
  footerContainer: {
    flex: 1,
    alignItems: 'center',
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
    fontWeight: "bold",
  },
  input: {
    padding: 10, // Reduced width for better layout
    height: 40,
    backgroundColor: '#333',
    color: '#fff',
    paddingHorizontal: 10,
    borderRadius: 5,
    marginBottom: 20,
    textAlign: 'center',
  },
  censoredContainer: {
    marginTop: 20,
    padding: 10,
    backgroundColor: '#444',
    borderRadius: 5,
    alignItems: 'center',
  },
  censoredText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  userContainer: {
    backgroundColor: '#444',
    padding: 10,
    borderRadius: 5,
    marginVertical: 5, // Reduced width for better layout
    alignItems: 'center',
  },
  userName: {
    flex: 1,
    color: '#fff',
    fontSize: 16,
  },
  userList: {
    marginTop: 20,
    padding: 10,
  },
  chatHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
    marginTop: 30,
  },
  message: {
    color: '#fff',
    fontSize: 14,
    marginVertical: 5,
  },
  messageList: {
    padding: 10,
  },
});
