import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Course {
  id: number;
  name: string;
  code: string;
  credits: number;
  grade: string;
}

@Injectable({
  providedIn: 'root'
})
export class CourseService {
  private apiUrl = 'https://jsonplaceholder.typicode.com/posts?_limit=5';

  constructor(private http: HttpClient) {}

  getCourses(): Observable<Course[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map(posts => 
        posts.map(post => ({
          id: post.id,
          name: post.title.split(' ').slice(0, 3).map((w: string) => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
          code: `CS${100 + post.id}`,
          credits: (post.id % 2 === 0) ? 4 : 3,
          grade: ['A', 'B', 'A+', 'B+', 'A'][post.id % 5]
        }))
      )
    );
  }
}
