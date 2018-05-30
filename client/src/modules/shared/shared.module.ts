// import angular modules
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// import third party modules
import { FlexLayoutModule } from '@angular/flex-layout';

// import custom mdodules
import { MaterialModule } from './material.module';

// import directives
import { IfOnDomDirective } from './directives/if-on-dom/if-on-dom.directive';
import { PerfectScrollbarDirective } from './directives/perfect-scrollbar/perfect-scrollbar.directive';


const MODULES = [
  CommonModule,
  MaterialModule,
  FlexLayoutModule
]

const DIRECTIVES = [
  IfOnDomDirective,
  PerfectScrollbarDirective
]

@NgModule({
  imports: [
    ...MODULES
  ],
  exports: [
    ...MODULES,
    ...DIRECTIVES
  ],
  declarations: [
    ...DIRECTIVES
  ]
})
export class SharedModule { }
