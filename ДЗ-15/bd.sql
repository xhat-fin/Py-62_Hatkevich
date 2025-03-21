CREATE TABLE authors (
    id serial PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30)
);

CREATE TABLE books(
    id serial PRIMARY KEY,
    title VARCHAR(30),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors (id)
);

CREATE TABLE sales(
    id serial PRIMARY KEY,
    book_id INT,
    quantity INT,
    FOREIGN KEY (book_id) REFERENCES books (id)
);


INSERT INTO authors (first_name, last_name) VALUES ('Федор','Достоевский'),
('Виктор','Гюго'),
('Александр','Дюма'),
('Алексей','Марков');

--автор без книг
INSERT INTO authors (first_name, last_name) VALUES ('Хаткевич', 'Никита');

INSERT INTO books(title, author_id)
VALUES ('Идиот', 1),
('Братья Карамазовы', 1),
('Человек, который смеется', 2),
('Три мушкетера', 3),
('Граф Монте Кристо', 3),
('Жлобология', 4),
('Хулиномика', 4),
('Криптвоюматика', 4),
('Лягушка, слон и брокколи', 4);

--книга без автора
INSERT INTO books(title) VALUES ('Тлен');


--било ошибку при создании таблицы books, id сместились и начались не с 1, а с 10
INSERT INTO sales(book_id, quantity) VALUES (10, 20), (11, 10), (12, 7), (13, 1), (14, 100), (15, 3), (16, 12), (17, 90), (18, 63);

--all books and authors
select title, first_name, last_name from books join authors on books.author_id = authors.id;

select concat(first_name,' ',last_name), title  from authors left join books on authors.id = books.author_id;

select concat(first_name,' ',last_name), title  from authors right join books on authors.id = books.author_id;


--множественный джоин по книгам авторам и продажам
select title, concat(first_name,' ',last_name), quantity from books left JOIN authors on books.author_id = authors.id LEFT JOIN sales on sales.book_id = books.id order by quantity DESC;


--сумма книг по авторам
select concat(first_name,' ',last_name), SUM(quantity)
from books JOIN authors
on books.author_id = authors.id
JOIN sales
on sales.book_id = books.id
GROUP BY concat(first_name,' ',last_name) order by SUM(quantity) DESC;


--сумма продаж по автору с учетом авторов без продаж
select concat(first_name,' ',last_name), SUM(quantity)
from authors left JOIN books
on books.author_id = authors.id
left JOIN sales
on sales.book_id = books.id
GROUP BY concat(first_name,' ',last_name) order by SUM(quantity) DESC;


-- подзапросы -> автор самых продаваемых книг
select concat(first_name,' ',last_name), SUM(quantity) from authors a
left join books b on a.id=b.author_id
LEFT JOIN sales s on b.id = s.book_id
group by concat(first_name,' ',last_name) HAVING SUM(quantity) = (
    select MAX(sum_q) from (
        select
        SUM(quantity) as sum_q from authors a
        left join books b on a.id = b.author_id
        left join sales s on b.id = s.book_id GROUP BY a.id
        )
    );


select b.title, SUM(s.quantity) as "Кол-во продаж" from books b
left join sales s on b.id = s.book_id
group by b.title HAVING SUM(s.quantity) > (
    select ROUND(AVG(quantity),0)
    from books b
    left JOIN sales s on b.id = s.book_id) order by SUM(s.quantity) DESC;