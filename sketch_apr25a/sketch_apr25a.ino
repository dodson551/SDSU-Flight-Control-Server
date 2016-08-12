const int ledPin = 13;
String read_string, max_X, min_X, max_Y, min_Y, max_Fwd, max_Rev;
int maxFwd = 0;
int maxRev = 0;
int maxX = 0;
int minX = 0;
int maxY = 0;
int minY = 0;

void setup() {
  
  // put your setup code here, to run once:
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
  Serial.println("All values are zero.");
  
}

void loop() {
 
  // put your main code here, to run repeatedly:
  while (Serial.available()) {
    delay(3);
    if (Serial.available() > 0) {
      char c = Serial.read();
      read_string += c;
    }
  }

  if (read_string.length() > 0) {
    Serial.println(read_string);

    max_X = read_string.substring(0, 3); // get first 3 characters
    min_X = read_string.substring(3, 6); // get next 3 characters
    max_Y = read_string.substring(6, 9);
    min_Y = read_string.substring(9, 12);
    max_Fwd = read_string.substring(12, 15);
    max_Rev = read_string.substring(15, 18);

    maxX = max_X.toInt();
    minX = min_X.toInt();
    maxY = max_Y.toInt();
    minY = min_Y.toInt();
    maxFwd = max_Fwd.toInt();
    maxRev = max_Rev.toInt();

    Serial.println("The new variables are: ");
    Serial.print("Max X: ");
    Serial.println(maxX);
    Serial.print("Min X: ");
    Serial.println(minX);
    Serial.print("Max Y: ");
    Serial.println(maxY);    
    Serial.print("Min Y: ");
    Serial.println(minY);   
    Serial.print("Max Fwd: ");
    Serial.println(maxFwd);
    Serial.print("Max Rev: ");
    Serial.println(maxRev);   
    
  }
  read_string = "";
  /// im gay
  
}


