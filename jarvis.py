import http from '@ohos.net.http';

// Modello della risposta per evitare errori di compilazione
interface JarvisResponse {
  reply: string;
}

@Entry
@Component
struct Index {
  @State message: string = 'In attesa, Signore';
  @State isConnecting: boolean = false;
  @State arcColor: string = '#00FFFF';

  build() {
    Column() {
      // Reattore Arc (Bottone)
      Stack() {
        Circle()
          .width(160)
          .height(160)
          .fill(Color.Transparent)
          .stroke(this.isConnecting ? '#FF4500' : this.arcColor)
          .strokeWidth(8)
          .shadow({ radius: 20, color: this.arcColor })
        
        Text(this.isConnecting ? "..." : "JARVIS")
          .fontSize(22)
          .fontColor(this.arcColor)
          .fontWeight(FontWeight.Bold)
      }
      .margin({ top: 50 })
      .onClick(() => {
        this.inviaComandoAlCloud("Status sistemi");
      })

      // Risposta testuale
      Scroll() {
        Text(this.message)
          .fontSize(16)
          .fontColor(Color.White)
          .textAlign(TextAlign.Center)
          .width('90%')
      }
      .margin({ top: 20 })
      .height(120)
    }
    .width('100%')
    .height('100%')
    .backgroundColor(Color.Black)
  }

  inviaComandoAlCloud(comando: string) {
    if (this.isConnecting) return;
    
    this.isConnecting = true;
    this.message = "Contatto il Cloud...";
    
    let httpRequest = http.createHttp();
    
    // SOSTITUISCI CON IL TUO LINK REALE DI RENDER
    let url = "https://AIzaSyCPieozxxVAmm4oU2Y4JKjgpLUqk9GTvU4/ask";

    httpRequest.request(
      url,
      {
        method: http.RequestMethod.POST,
        header: { 'Content-Type': 'application/json' },
        extraData: JSON.stringify({ "command": comando }),
        expectDataType: http.HttpDataType.STRING // Dice all'app di aspettarsi testo
      },
      (err, data) => {
        this.isConnecting = false;
        
        if (!err && data.responseCode === 200) {
          try {
            // Conversione sicura del JSON
            const result = JSON.parse(data.result as string) as JarvisResponse;
            this.message = result.reply;
            this.arcColor = '#00FFFF';
          } catch (e) {
            this.message = "Errore decodifica risposta";
          }
        } else {
          this.message = "Errore: Connessione fallita";
          this.arcColor = '#FF0000';
        }
        
        // Pulizia memoria
        httpRequest.destroy();
      }
    );
  }
}
