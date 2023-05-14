import { Component, OnInit } from '@angular/core';
import { ArticlesService } from '../../services/articles.service';
import { ArticleDetailsComponent } from '../article-details/article-details.component';

@Component({
  selector: 'app-list-media',
  templateUrl: './list-media.component.html',
  styleUrls: ['./list-media.component.scss']
})
export class ListMediaComponent implements OnInit {
  public allArticles: any[] = [];
  toDisplay: any = null

  constructor(public articles: ArticlesService) { }

  async ngOnInit() {
    this.articles.getTitles().then((res) => {
      this.allArticles = res.titles;
    })
  }

  public selectedArticle: any = null;

  pickArticle(article: any) {
    this.selectedArticle = article 
  }

  async displayDetails(article: any) {
    this.toDisplay = article
    // this.similarArticles = await 
  }

}
