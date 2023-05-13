import { Component, OnInit } from '@angular/core';
import { ArticlesService } from '../../services/articles.service';
import { ArticleDetailsComponent } from '../article-details/article-details.component';

@Component({
  selector: 'app-list-media',
  templateUrl: './list-media.component.html',
  styleUrls: ['./list-media.component.scss']
})
export class ListMediaComponent implements OnInit {

  constructor(public articles: ArticlesService) { }

  ngOnInit(): void {
  }

  public selectedArticle: any = null;

  pickArticle(article: any) {
    this.selectedArticle = article 
  }

}
