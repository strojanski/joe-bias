import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListMediaComponent } from './list-media.component';

describe('ListMediaComponent', () => {
  let component: ListMediaComponent;
  let fixture: ComponentFixture<ListMediaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ListMediaComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListMediaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
