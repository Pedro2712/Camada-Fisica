int parity(char data) {
  int ones = 0;
  for(int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }
  return ones % 2;
}

void espera(){
  for(int i = 0; i < 2187; i++){
    asm("NOP");
  }
}
