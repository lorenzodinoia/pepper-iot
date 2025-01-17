import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgxEchartsModule } from 'ngx-echarts';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { RoomCardComponent } from './room-card/room-card.component';
import { BedCardComponent } from './bed-card/bed-card.component';
import { RoomComponent } from './room/room.component';
import { InmateSummaryComponent } from './inmate-summary/inmate-summary.component';
import { RoomTemperatureChartComponent } from './room-temperature-chart/room-temperature-chart.component';
import { RoomHumidityChartComponent } from './room-humidity-chart/room-humidity-chart.component';
import { RoomLuxChartComponent } from './room-lux-chart/room-lux-chart.component';
import { RoomVocChartComponent } from './room-voc-chart/room-voc-chart.component';
import { InmateComponent } from './inmate/inmate.component';
import { InmateTemperatureChartComponent } from './inmate-temperature-chart/inmate-temperature-chart.component';
import { InmateOxygenationChartComponent } from './inmate-oxygenation-chart/inmate-oxygenation-chart.component';
import { InmateBpmChartComponent } from './inmate-bpm-chart/inmate-bpm-chart.component';
import { InmatePressureChartComponent } from './inmate-pressure-chart/inmate-pressure-chart.component';
import { DatePipe } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatListModule } from '@angular/material/list';
import { MatSidenavModule } from '@angular/material/sidenav';
import { NavigationComponent } from './navigation/navigation.component';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { RoomNavItemComponent } from './room-nav-item/room-nav-item.component';
import { BedNavItemComponent } from './bed-nav-item/bed-nav-item.component'

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    RoomCardComponent,
    BedCardComponent,
    RoomComponent,
    InmateSummaryComponent,
    RoomTemperatureChartComponent,
    RoomHumidityChartComponent,
    RoomLuxChartComponent,
    RoomVocChartComponent,
    InmateComponent,
    InmateTemperatureChartComponent,
    InmateOxygenationChartComponent,
    InmateBpmChartComponent,
    InmatePressureChartComponent,
    NavigationComponent,
    RoomNavItemComponent,
    BedNavItemComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgxEchartsModule.forRoot({
      echarts: () => import('echarts')
    }),
    NgbModule,
    BrowserAnimationsModule,
    MatListModule,
    MatSidenavModule,
    LayoutModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule
  ],
  providers: [DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
