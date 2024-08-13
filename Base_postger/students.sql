CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    institute VARCHAR(100) NOT NULL,
    group_name VARCHAR(50) NOT NULL,
    course_number VARCHAR(10) NOT NULL,
    study_program VARCHAR(255) NOT NULL,
    manhole_cover TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
