import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './student-profile.component.html',
  styles: []
})
export class StudentProfileComponent implements OnInit {
  profileForm!: FormGroup;

  ngOnInit(): void {
    this.profileForm = new FormGroup({
      name: new FormControl('Gopika R', [Validators.required]),
      email: new FormControl('gopika.r@example.com', [Validators.required, Validators.email]),
      semester: new FormControl('6', [
        Validators.required, 
        Validators.min(1), 
        Validators.max(8)
      ])
    });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      console.log('Form Submitted successfully!', this.profileForm.value);
    }
  }

  // Getters for easy template checks
  get name() { return this.profileForm.get('name'); }
  get email() { return this.profileForm.get('email'); }
  get semester() { return this.profileForm.get('semester'); }
}
