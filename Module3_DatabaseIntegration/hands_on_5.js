
// MongoDB – CRUD, Aggregation & Indexes



// Task 1 : Create Database and Collection


use college_nosql

db.createCollection("feedback")


db.feedback.insertMany([

{
student_id:1,
course_code:"CS101",
semester:"2022-ODD",
rating:5,
comments:"Excellent teaching.",
tags:["challenging","well-structured","good-examples"],
submitted_at:new Date("2022-11-30"),
attachments:[
{filename:"notes.pdf",size_kb:240}
]
},

{
student_id:2,
course_code:"CS101",
semester:"2022-ODD",
rating:4,
comments:"Very informative.",
tags:["challenging","interesting"],
submitted_at:new Date("2022-11-29"),
attachments:[
{filename:"assignment.pdf",size_kb:120}
]
},

{
student_id:3,
course_code:"CS101",
semester:"2022-ODD",
rating:3,
comments:"Average.",
tags:["lengthy"],
submitted_at:new Date("2022-11-28"),
attachments:[
{filename:"lab.pdf",size_kb:200}
]
},

{
student_id:4,
course_code:"CS102",
semester:"2022-ODD",
rating:5,
comments:"Loved the subject.",
tags:["good-examples","easy"],
submitted_at:new Date("2022-11-27"),
attachments:[
{filename:"db.pdf",size_kb:310}
]
},

{
student_id:5,
course_code:"CS102",
semester:"2022-ODD",
rating:2,
comments:"Too difficult.",
tags:["hard","challenging"],
submitted_at:new Date("2022-11-26"),
attachments:[
{filename:"report.pdf",size_kb:150}
]
},

{
student_id:6,
course_code:"CS103",
semester:"2021-EVEN",
rating:4,
comments:"Good.",
tags:["oop","coding"],
submitted_at:new Date("2021-12-10"),
attachments:[
{filename:"java.pdf",size_kb:180}
]
},

{
student_id:7,
course_code:"ME101",
semester:"2022-ODD",
rating:1,
comments:"Needs improvement.",
tags:["boring"],
submitted_at:new Date("2022-11-20"),
attachments:[
{filename:"thermo.pdf",size_kb:160}
]
},

{
student_id:8,
course_code:"EC101",
semester:"2022-ODD",
rating:5,
comments:"Excellent lab sessions.",
tags:["practical","interesting"],
submitted_at:new Date("2022-11-18"),
attachments:[
{filename:"circuit.pdf",size_kb:170}
]
},

{
student_id:9,
course_code:"CS103",
semester:"2022-ODD",
rating:4,
comments:"Very useful.",
tags:["coding","practice"],
submitted_at:new Date("2022-11-17"),
attachments:[
{filename:"oopnotes.pdf",size_kb:210}
]
},

{
student_id:10,
course_code:"CS101",
semester:"2021-EVEN",
rating:5,
comments:"Best course.",
tags:["challenging","excellent"],
submitted_at:new Date("2021-12-15")
},

{
student_id:11,
course_code:"CS102",
semester:"2022-ODD",
rating:3,
comments:"Good.",
tags:["database","sql"],
submitted_at:new Date("2022-11-16"),
attachments:[
{filename:"sql.pdf",size_kb:130}
]
}

])

// Verify Insert

db.feedback.countDocuments()


// task -2 

// READ

//65. Rating = 5

db.feedback.find({rating:5})

//66. CS101 with tag challenging

db.feedback.find({
course_code:"CS101",
tags:"challenging"
})

//67. Projection

db.feedback.find(
{},
{
_id:0,
student_id:1,
course_code:1,
rating:1
})


// UPDATE


//68. Add needs_review=true

db.feedback.updateMany(
{
rating:{$lt:3}
},
{
$set:{needs_review:true}
}
)

//69. Push reviewed tag

db.feedback.updateMany(
{
needs_review:true
},
{
$push:{tags:"reviewed"}
})



// DELETE


//70. Delete semester 2021-EVEN

db.feedback.deleteMany({
semester:"2021-EVEN"
})


// task -3
db.feedback.aggregate([

{
$match:{
semester:"2022-ODD"
}
},

{
$group:{
_id:"$course_code",
avg_rating:{
$avg:"$rating"
},
feedback_count:{
$sum:1
}
}
},

{
$sort:{
avg_rating:-1
}
}

])


db.feedback.aggregate([

{
$match:{
semester:"2022-ODD"
}
},

{
$group:{
_id:"$course_code",
avg_rating:{
$avg:"$rating"
},
feedback_count:{
$sum:1
}
}
},

{
$project:{
_id:0,
course_code:"$_id",
average_rating:{
$round:["$avg_rating",1]
},
feedback_count:1
}
},

{
$sort:{
average_rating:-1
}
}

])

db.feedback.aggregate([

{
$unwind:"$tags"
},

{
$group:{
_id:"$tags",
count:{
$sum:1
}
}
},

{
$sort:{
count:-1
}
}

])

db.feedback.createIndex({
course_code:1
})