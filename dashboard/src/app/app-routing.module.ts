import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { InmateComponent } from './inmate/inmate.component';
import { RoomComponent } from './room/room.component';

const routes: Routes = [
  {path: "home", component: HomeComponent},
  {path: "room/:id", component: RoomComponent},
  {path: "inmate/:id", component: InmateComponent},

  {path: "**", redirectTo: "home"}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
