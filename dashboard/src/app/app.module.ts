import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { HomeComponent } from './home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { RoomCardComponent } from './room-card/room-card.component';
import { BedCardComponent } from './bed-card/bed-card.component';
import { RoomComponent } from './room/room.component';
import { InmateSummaryComponent } from './inmate-summary/inmate-summary.component';

@NgModule({
  declarations: [
    AppComponent,
    ToolbarComponent,
    HomeComponent,
    RoomCardComponent,
    BedCardComponent,
    RoomComponent,
    InmateSummaryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
