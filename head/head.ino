#include "Data.h"
#include "Servo.h"

Servo s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10;
char data;
char buff[255];
int iCh = 0;

void attach()
{
 s0.attach(40);
 s1.attach(41);
 s2.attach(42); 
 s3.attach(43);
 s4.attach(44); 
 s5.attach(45);
 s6.attach(46);
 s7.attach(47);
 s8.attach(48);
 s9.attach(49);
 s10.attach(50);
 start();
}

void start()
{
  s10.write(0);
  s9.write(10);
  s7.write(0);
  s0.write(80);
  s6.write(120);
  s5.write(80);
  s4.write(50);
  s3.write(60);
  s2.write(50);
  s1.write(80);
  s8.write(80);
}

void xinchao()
{
   for(int i=1;i<=5;i++)
 { 
  s10.write(20);
  s9.write(100);
  s7.write(80);
  s0.write(80);
  s6.write(120);
  s5.write(60);
  s4.write(30);
  s3.write(60);
  s2.write(30);
  s1.write(150);char data;
  s8.write(115);
  delay(2000);
  s8.write(65);
  delay(2000);
 }
 s10.write(0);
  s9.write(10);
  s7.write(0);
  s0.write(80);
  s6.write(120);
  s5.write(80);
  s4.write(50);
  s3.write(60);
  s2.write(50);
  s1.write(80);
  s8.write(80);
}
void a()
{
  
}

void b()
{
  
}

void c()
{
  
}
void setup()
{
  Serial.begin(9600);
  attach();
  Data* data = Data::getInstance();
  data->addAction('a', a);
  data->addAction('b', b);
  data->addAction('c', c);
}

String rcv = ""; // chuoi nhan duoc
double secAudio; // thoi gian cau tra loi
String text; // cau tra loi
bool isStarted = false;
void test()
{
  if (!isStarted)
  {
    xinchao();
    isStarted = true;      
  }
}

bool isValidCharacter(char ch) {
  return (ch >= '0' && ch <= '9') || ch == '.' || ch == '_' || ch == '|' || (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z');
}

void analyseCommand(double &secAudio, String &ques, String &ans) {
  if(ques == "xinchao")
  {
    xinchao();      
  }
//    Data* data = Data::getInstance();
//    int length_text = text.length();
//    Action action;
//    for (int i = 0; i < length_text; ++i)
//    {
//      action = data->act(text[i]);
//      if (action) {
//        action();
//      } else {
//        delay(500);
//      }
//    }  
}

void build()
{
  while (Serial.available() > 0)
  {
    data = Serial.read();

    if (data == '\r') {
      Serial.read(); // read '\n' charater
      while (Serial.available()) Serial.read();
      
      String sSecAudio = "";
      String ques = "";
      String ans = "";
      
      int i;
      for (i = 0; buff[i] != '|'; ++i)
      {
        sSecAudio += buff[i];
      }
      for (i += 1; buff[i] != '|'; ++i)
      {
        ques += buff[i];
      }
      for (i += 1; i < iCh; ++i)
      {
        ans += buff[i];
      }
      double secAudio = sSecAudio.toDouble();

      analyseCommand(secAudio, ques, ans);
      Serial.println("OK");
      buff[iCh] = '\0';
      iCh = 0;
    }
    else if (isValidCharacter(data)) buff[iCh++] = data;
  }
}

void loop()
{
  build();
}
