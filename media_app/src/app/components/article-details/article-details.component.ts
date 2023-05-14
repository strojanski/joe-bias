import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-article-details',
  templateUrl: './article-details.component.html',
  styleUrls: ['./article-details.component.scss']
})
export class ArticleDetailsComponent implements OnInit {


  @Input() article: any = null;
  


  constructor() { }

  ngOnInit(): void {
  }


}
