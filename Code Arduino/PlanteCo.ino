

//Including the libraries

#include <DHT.h>                                  // DHT sensor library - Version: Latest 
#include <DHT_U.h>

#include <ThingerWifi.h>                          // thinger.io library
#include <WiFi.h>


#include "Wire.h"
    #include <Sparkfun_APDS9301_Library.h>        // SparkFun APDS-9301 Lux Sensor 
    APDS9301 apds;
    #define INT_PIN 10                            // We will connect the sensor in the pin 10
                      
   
    
                     
#define DHTPIN 2                                  //we will connect the dht sensor on the pin 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define _DEBUG_
#define _DISABLE_TLS_
#define THINGER_USE_STATIC_MEMORY
#define THINGER_STATIC_MEMORY_SIZE 512
#define ThingerWifi ThingerWifiClient


#define USERNAME "guigui"                       //setting the connection's informations, in order to connect to thinger.io
#define DEVICE_ID "arduino2"                    //setting the connection's informations, in order to connect to thinger.io
#define DEVICE_CREDENTIAL "arduino2"            //setting the connection's informations, in order to connect to thinger.io

#define SSID "gui"                              //setting the SSID variable
#define SSID_PASSWORD "guillaume"               //setting the SSID_PASSWORD variable

ThingerWifi thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL);

int temp = 0;                                   //setting streamed values
int hum = 0;                                    //setting streamed values
int humSol = 0;                                 //setting streamed values
  
void setup() {
  Serial.begin(9600);                           //defining the baud rate 
  
  thing.add_wifi(SSID, SSID_PASSWORD);          // configure wifi network




  thing["APDS9301"] >> [](pson& out){
    out["APDS9301"] = apds.readCH0Level();      //Defining the name of the variable streamed to thinger.io
  };
  
  dht.begin();
  thing["DHT11Hum"] >> [](pson& out){
    out["DHT11Hum"] = hum;                      //Defining the name of the variable streamed to thinger.io

  };
  thing["DHT11Cel"] >> [](pson& out){
    out["DHT11Cel"] = temp;                     //Defining the name of the variable streamed to thinger.io
  };
  
  dht.begin();
  thing["SoilMoistureV1.0"] >> [](pson& out){
    out["SoilMoistureV1.0"] = humSol;           //Defining the name of the variable streamed to thinger.io
  };
  
  
  
  
  delay(5);                                     // The CCS811 need  a brief delay after startup.
      Wire.begin();


                                        // APDS9301 sensor setup.
      apds.begin(0x39); 
      
      apds.setGain(APDS9301::LOW_GAIN);                         // Set the gain to low.

      apds.setIntegrationTime(APDS9301::INT_TIME_13_7_MS);      // Set the integration time to the shortest interval.



      apds.setLowThreshold(0);                                  // Sets the low threshold to 0.
      
      apds.setHighThreshold(500);                               // Sets the high threshold to 500. 
      
      apds.setCyclesForInterrupt(1);                            // A single reading in the threshold range will cause an interrupt to trigger.

      apds.enableInterrupt(APDS9301::INT_ON);                   // Enable the interrupt.
      apds.clearIntFlag();
      
      
      

    
}

void loop() {
  thing.handle();
  
  
  
  if (isnan(dht.readTemperature())){   //checking if the captor is well pluged
      temp = -1;
  }
  else{
    temp = dht.readTemperature();
  }
  
  
  
  if (isnan(dht.readHumidity())){       //checking if the captor is well pluged
      hum = -1;
  }
  else{
    hum = dht.readHumidity();
  }




  if (analogRead(0)>600){               //checking if the captor is well pluged
    humSol = -1;
  }
  else{
    humSol = analogRead(0);
  }
    
  thing.stream(thing["DHT11Hum"]);              //Streaming the value to thinger.io
  thing.stream(thing["DHT11Cel"]);              //Streaming the value to thinger.io
  thing.stream(thing["APDS9301"]);              //Streaming the value to thinger.io
  thing.stream(thing["SoilMoistureV1.0"]);      //Streaming the value to thinger.io
  
  
  
  
  static unsigned long outLoopTimer = 0;
      apds.clearIntFlag();                          

     
      if (millis() - outLoopTimer >= 1000)      //Printing value on the local monitor every second
      {
        
        outLoopTimer = millis();
        
        int val;
        val = analogRead(0); 
        Serial.print("Humidity sol: ");
        Serial.println(val); 

        Serial.print("Flux lumineux: ");
        Serial.println(apds.readCH0Level());
        
        Serial.print("Humidity: ");
        Serial.println(dht.readHumidity());
        
        Serial.print("Temperature: ");
        Serial.println(dht.readTemperature());
      };

} 
