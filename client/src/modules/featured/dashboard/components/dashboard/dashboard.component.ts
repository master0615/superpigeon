import { Component, OnInit } from '@angular/core';
import { ConfigService } from '../../../../core/services/config/config.service';

@Component({
  selector: 'dashboard-component',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {

  constructor(private config: ConfigService) {
    this.config.setSettings({
      layout: {
        navigation: 'true',
        toolbar: 'true',
        footer: 'true'
      }
    });
  }

  ngOnInit() {
  }
}
