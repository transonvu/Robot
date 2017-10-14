boolean readline(char c, String &s, double &secAudio, String &text)
{
  if (c > 0) 
  {
    switch (c) 
    {
      case '\n':
      {
        String sSecAudio = "";
        text = "";
        int length = s.length();
        int i;
        for (i = 0; s[i] != ' '; ++i)
        {
          sSecAudio += s[i];
        }
        for (i += 1; i < length; ++i)
        {
          text += s[i];
        }
        secAudio = sSecAudio.toDouble();
      }
        return true;
      default:
        s += c;
        break;
    }
  }
  // No end of line has been found, so return -1.
  return false;
}


void setup()
{
  Serial.begin(9600);
}

String rcv = "";
double secAudio;
String text;

void loop()
{
  char c = Serial.read();
  if (readline(c, rcv, secAudio, text))
  {
    Serial.println(rcv);
    rcv = "";
    Serial.println(secAudio); // thoi gian cau tra loi
    Serial.println(text); // cau tra loi
    Serial.println("0"); //Gui bao cho anh biet em da hoan thanh xong
  }
}
