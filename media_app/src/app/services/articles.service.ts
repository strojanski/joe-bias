import { Injectable } from '@angular/core';
import { response } from 'express';
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
    return fetch(`${this.API_URL}/`).then((response) => {
      return response.json();
    })
  }
  // async getTitles() {
  //   const response = await fetch(`${this.API_URL}/`);
  //   const data = await response.json();
  //   console.log("Got data")
  //   return data.titles;
  // }

  /**
   * Returns an object representing the article content with the given title, also has content field
   */
  async getArticleContent(publisher: string) {
    const response = await fetch(`${this.API_URL}/similar/${publisher}`)
    const data = await response.json();
    return data.titles;
  }

  /**
   * Returns bias of a given article
   */
  // async getBias(title: string): Promise<any> {
  //   const reponse = await fetch(`${this.API_URL}/bias/${title}`)
  //   const data = await response.json()
  //   return data.bias;
  // }

  // async getSimilar(article: any) {
  //   const reponse = await fetch(`${this.API_URL}/similar/${article}`)
  //   const data = await response.json()
  //   return data.data;
  // }


}
