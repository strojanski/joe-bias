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
  rating: any = null
  url: any = null;

  constructor(public articles: ArticlesService) { }

  combinedArray: any[] = [];
  async ngOnInit() {
    this.articles.getTitles().then((res) => {
      this.allArticles = res.titles;
      this.combinedArray = this.pairElements(this.allArticles);
    })
  }
  bgimg: any = "none"
  media_name: any = null
  bg: any = "white"
  public selectedArticle: any = null;

  pickArticle(article: any) {
    this.selectedArticle = article 
  }

  async displayDetails(article: any) {
    this.toDisplay = article
    this.url = this.toDisplay.url;
    this.rating = null
    this.media_name = article.media_nam
    this.bg = "white"
    // this.similarArticles = await 
  }

  async getRating() {
    console.log(this.toDisplay)
    this.rating = (await this.articles.getBias(this.toDisplay)).bias * 20;
    console.log(this.rating)
    if (isNaN(this.rating)) {
      this.rating = 0.11123124;
    }
    this.getBgColor()
  }

  isAlpha(str: string) {
    return  /^[a-zA-Z0-9]+$/.test(str)
  }

  getBgColor() {
    if (this.rating != null) {
      if (this.rating < 0) {
        this.bgimg = "/bernie.webp"
        this.bg = "red"
      }
      else {
        this.bg = "lightblue"
        this.bgimg = "/trump.jpg"
      } 
        
    }

    console.log(this.bg)
  }

  pairElements(elements: any[]): any[] {
    const pairedElements = [];
    for (let i = 0; i < elements.length; i += 2) {
      const element1 = elements[i];
      const element2 = elements[i + 1];
  
      const pairedElement = {
        element1: element1,
        element2: element2
      };
  
      pairedElements.push(pairedElement);
    }
    return pairedElements;
  }
}
