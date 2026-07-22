import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';
import { CourseService, Course } from '../../services/course.service';
import { CourseCardComponent } from '../course-card/course-card.component';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  templateUrl: './course-list.component.html',
  styles: []
})
export class CourseListComponent implements OnInit, OnDestroy {
  courses: Course[] = [];
  searchTerm: string = '';
  loading: boolean = true;
  error: string | null = null;
  private subscription!: Subscription;

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loading = true;
    this.subscription = this.courseService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load courses. Please try again later.';
        this.loading = false;
        console.error(err);
      }
    });
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe(); // Prevent memory leaks
    }
  }

  get filteredCourses(): Course[] {
    return this.courses.filter(course =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}
