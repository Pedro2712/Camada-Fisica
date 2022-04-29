void setup() {
  // put your setup code here, to run once:
  // 01100001 = a
  // 01000001 = A
  
  pinMode(2, OUTPUT);
  char letra = 'a';

  int paridade= parity(letra)
  Serial.println(paridade);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(2, HIGH);
  digitalWrite(2, LOW);
  espera();

  digitalWrite(2, HIGH);
  espera();

  digitalWrite(2, LOW);
  espera();

  digitalWrite(2, LOW);
  espera();

  digitalWrite(2, LOW);
  espera();

  digitalWrite(2, LOW);
  espera();

  digitalWrite(2, HIGH);
  espera();

  digitalWrite(2, HIGH);
  espera();

  digitalWrite(2, LOW);
  espera();

  if (paridade == 1){
    digitalWrite(2, HIGH);
  } else{
    digitalWrite(2, LOW);
  }
  espera();
  
  digitalWrite(2, HIGH);
  delay(2000);
}