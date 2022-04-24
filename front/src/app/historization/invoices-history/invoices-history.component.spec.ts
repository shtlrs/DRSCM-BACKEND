import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvoicesHistoryComponent } from './invoices-history.component';

describe('InvoicesHistoryComponent', () => {
  let component: InvoicesHistoryComponent;
  let fixture: ComponentFixture<InvoicesHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InvoicesHistoryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InvoicesHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
