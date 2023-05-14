import { Injectable } from '@angular/core';
import { Article } from '../Article';

@Injectable({
  providedIn: 'root'
})
export class ArticlesService {

  // Array of articles
  public articles: Article[] = []
  private API_URL = 'http://localhost:5000';

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


  /**
   * Returns a list of Article objects representing the most trending articles
   */
  async getTitles() {
    return fetch(`${this.API_URL}/titles`).then((response) => {
      return response.json();
    }
  )}


  /**
   * Returns an object representing the article content with the given title, also has content field
   */
  async getArticleContent(title: string) {
    return fetch(`${this.API_URL}/article/${title}`).then((response) => {
      return response.json();
    });
  }

  /**
   * Returns bias of a given article
   */
  async getBias(title: string): Promise<any> {
    return fetch(`${this.API_URL}/bias/${title}`).then((response) => {
      return response.json();
    });
  }



}
