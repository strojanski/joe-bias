import { Injectable } from '@angular/core';
import { Article } from '../Article';

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {

  // Array of articles
  public articles: Article[] = []


  constructor() {
    this.articles.push({
      title: 'Article 1',
      description: 'This is the first article',
      time: '2021-01-01',
      url: 'https://www.google.com',
      publisher: 'Google'
   })

   this.articles.push({
    title: 'Article 1',
    description: 'This is the first article',
    time: '2021-01-01',
    url: 'https://www.google.com',
    publisher: 'Google'
 })
  }

  
  // TODO api call to get articles

  get getArticles() {
    return this.articles;
  }




}
