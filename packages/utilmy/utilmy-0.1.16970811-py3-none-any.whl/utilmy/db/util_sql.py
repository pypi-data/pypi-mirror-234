""" SQL Examples
Doc::

    List of SQL

    ---- --1: MoM Percent Change 
    **Context:** Often times it's useful to know how much a key metric, 
    such as monthly active users, changes between months. Say we have a table `logins` in the form: 

    | user_id | date       |
    |---------|------------|
    | 1       | 2018-07-01 |
    | 234     | 2018-07-02 |
    | 1       | 2018-07-02 |
    | ...     | ...        |
    | 234     | 2018-10-04 |
    **Task**: Find the month-over-month percentage change for monthly active users (MAU). 
    -- Solution:-- 


    -------- solution OK 
    SELECT  tyear, tmonth,  (n_user / lag(n_user,1) -1.0)*100.0   as mau_pct_chg
    FROM (
    select tyear, tmonth  count(user_id) as n_user

    FROM  (
      Select   year(date) as tyear, month(date) as tmonth, user_id
      from users as t1
    )
    group by year,month
    ORDER BY year, month
    )


    -------- Solution with n_users = 0 for some months
    -------- generate the 12 month ??? manually, how you would do ?
    (
      SELECT YEAR(a.my_date) AS my_year, MONTH(a.my_date) AS my_month 
      FROM
      (
        SELECT curdate() - INTERVAL (a.a + (10 * b.a) + (100 * c.a)) MONTH as my_date
        FROM (
              select 0 as a union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as a
        
              CROSS JOIN (select 0 as a union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as b
        
              CROSS JOIN (select 0 as a union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as c

      ) a









    ---- --2: Tree Structure Labeling   
    **Context:** Say you have a table `tree` with a column of nodes and a column corresponding parent nodes 

    ```
    node   parent
    1       2
    2       5
    3       5
    4       3
    5       NULL 
    ```

    **Task:** Write SQL such that we label each node as a “leaf”, “inner” or “Root” node, such that for the nodes above we get: 

    ```
    node    label  
    1       Leaf
    2       Inner
    3       Inner
    4       Leaf
    5       Root
    ```

    (Side note: [this link](http://ceadserv1.nku.edu/longa//classes/mat385_resources/docs/trees.html) has more details on Tree data structure terminology. Not needed to solve the problem though!)
    * * *
    -- Solution:-- 





























    ---- --3: Retained Users Per Month (multi-part)
    ** [“Using Self Joins to Calculate Your Retention, Churn, and Reactivation Metrics”]
    (https://www.sisense.com/blog/use-self-joins-to-calculate-your-retention-churn-and-reactivation-metrics/) 
    ------ Part 1: 
    **Context:** Say we have login data in the table `logins`: 
    | user_id | date       |
    |---------|------------|
    | 1       | 2018-07-01 |
    | 234     | 2018-07-02 |
    | 1       | 2018-07-02 |
    | ...     | ...        |
    | 234     | 2018-10-04 |
    **Task:** Write a query that gets the number of retained users per month. In this case, retention for a given month is defined as the number of users who logged in that month who also logged in the immediately previous month. 

    -- Solution:--   
    1)  pelase confirm if my code is OK or not ( correct or NOT) - yes, looks good
    WITH  monthly_users
    AS(       
                select tyear, tmonth, tyear_prev, tmonth_prev  count(user_id) as n_user
    FROM  (
      Select   year(date) as tyear, month(date) as tmonth, user_id,
                  year(add_month(date, -1))    as   tyear_prev,    ------ added prev month here using add_month
                  month(add_month(date, -1)) as   tmonth_prev             
      from users as t1
    )
    group by tyear, tmonth, tyear_prev, tmonth_prev
    ORDER BY tyear, tmonth, tyear_prev, tmonth_prev
    ) ,

    SELECT  tyear, tmonth, n_user
    FROM      monthly_users as t1
    INNER JOIN (  -- user in both months
      SELECT * FROM monthly_users
    ) as t2 
    ON       
        t2.user_id          =  t1.user_id
        AND  t2.year     =  t1.year_prev   ------ previous month
        AND  t2.month  =  t1.month_prev
      

    2nd) (ie more optimized)
    Part1: retained
    WITH monrhtly_user AS
    (
        
    )
    Select
      tyear, tmonth, count(u.user_id) AS n_user
    From monthly_users AS t1
    INNER Join monthly_users AS t2   
      ON   t1.user_id = t2.user_id 
      AND CAST(month(t1.date) as INT) = cast(month(DATEADD(month, -1, t1.date)) as INT) 
      AND CAST(year(t1.date)  as INT) = cast(year(DATEADD(month, -1, t1.date))  as INT) 
    
      
    With dateadd you don’t need to separate year and month
    Be careful to consider multi-year data, or generic case in your solutions,
    Ok, it;sa similar to my solution with date operator on the condition + dateadd
    Using datediff



    ------ Part 2: 
    **Task:** Now we’ll take retention and turn it on its head: Write a query to find how many users last month *did not* come back this month. i.e. the number of churned users.  
    -- Solution:-- 

    SELECT   tyear, tmonth, count(user_id)
    FROM       users t1                 ------   (Previous month)

    LEFT JOIN users   AS t2       ------   Next month
    ON   
      t2.user_id = t1.user_id
      AND  MONTH( t2.date) =  MONTH( dateadd(month, +1,  t1.date   )
      AND  YEAR(  t2.date)   =  YEAR( dateadd(month,  +1,    t1.date   )
    WHERE
            t2.user_id IS NULL

    GROUP BY tyear, tmonth


    trick:         LEFT JOIN    t2.user_id is NULL       ===  user_id NOT IN (  Select user_id ...)
    Dont always limit just to the text description (ie  natural Genealization is better,  more practice == real world thing,)



    ------ Part 3: 
    **Note:** this question is probably more complex Consider it a challenge problem

    **Context**: Data engineering has decided to give you a helping hand by creating a table of churned users per month, `user_churns`. If a user is active last month but then not active this month, then that user gets an entry for this month. `user_churns` has the form: 
    | user_id | month_date |
    |---------|------------|
    | 1       | 2018-05-01 |
    | 234     | 2018-05-01 |
    | 3       | 2018-05-01 |
    | 12      | 2018-05-01 |
    | ...     | ...        |
    | 234     | 2018-10-01 |
    ```

    **Task**: You now want to do a cohort analysis of active users this month *who have been reactivated users in the past*. Create a table that contains these users. You may use the tables `user_churns` as well as `logins` to create this cohort. In Postgres, the current timestamp is available through `current_timestamp`.
    * * *
    -- Solution:-- 



















    ---- --4: Cumulative Sums 
    Cash Flow modeling in SQL”](https://www.sisense.com/blog/cash-flow-modeling-in-sql/)t 

    **Context:** Say we have a table `transactions` in the form:
    | date       | cash_flow |
    |------------|-----------|
    | 2018-01-01 | -1000     |
    | 2018-01-02 | -100      |
    | 2018-01-03 | 50        |
    | ...        | ...       |
    ```
    Where `cash_flow` is the revenues minus costs for each day. 

    **Task: **Write a query to get *cumulative* cash flow for each day such that we end up with a table in the form below: 
    | date       | cumulative_cf |
    |------------|---------------|
    | 2018-01-01 | -1000         |
    | 2018-01-02 | -1100         |
    | 2018-01-03 | -1050         |
    | ...        | ...           |
    -- Solution:--   http://sqlfiddle.com/--!18/abdce/1
    Below is correct ???






    -------- using Self-JOIN
    with cf_table AS     ------ 1 cashflow per date
    select date, sum(cash_flow) as cf    
    from      cash_flows as t1
    GROUP BY date
    ORDER by date
    ,
    SELECT t1.date,  sum(t2.cf) as cumulateive_cf  
    FROM cf_table as t1

    INNER JOIN (
          Select   *  FROM cf_table
          )  AS t2 
        ON  t2.date <= t1.date   ----  OK: sum of previous days
    GROUP BY t1.date   
    

    -------- Solution by Yvan
    SELECT 
    t.date [date], 
    SUM(tt.cash_flow) as cumulative_cf 
    FROM transactions t1
    INNER JOIN transactions t2 
        ON t2.date  <=    t1.date   ------ only past dates 
    GROUP BY t.date 
    ORDER BY t.date ASC
      
    It;s more logical to  use   <=      ie previous date sum.  :  Cum sum of past dates. !!!
      









    ---- --5: Rolling Averages
    ”(https://www.sisense.com/blog/rolling-average/) blog post 
    **Note:** there are different ways to compute rolling/moving averages. Here we'll use a preceding average which means that the metric for the 7th day of the month would be the average of the preceding 6 days and that day itself. 
    **Context**: Say we have table `signups` in the form: 
    | date       | sign_ups |
    |------------|----------|
    | 2018-01-01 | 10       |
    | 2018-01-02 | 20       |
    | 2018-01-03 | 50       |
    | ...        | ...      |
    | 2018-10-01 | 35       |
    **Task**: Write a query to get 7-day rolling (preceding) average of daily sign ups. 


    -------- Solution 1
    SELECT 
    t1.date, 
    AVG(t2.sign_ups) average_sign_ups 
    FROM signups AS t1
    INNER JOIN signups AS t2 
          ON   t1.date   >=  dateadd(day, -6, t2.date)  ---- preceding 6 days
          AND  t1.date   <=  t2.date                    ---- that day itself. 
    GROUP BY t1.date

    ------ ok. it;s generic way to write moving average.
    Matchin Descpriotn parameters   :    preceding 6 days
    == more intuitive, easier to cross check



    ------ Solution using windowing ( in Hive SQL), OK
    select date
              ,AVG(sign_ups)  OVER (  ORDER BY date  
                                                      ROWS BETWEEN  6 PRECEDING AND CURRENT ROW) ------ not familiar with this syntax, for pseudocode OK
              as signup_avg_7day
    FROM table t1

    ------ With Missing days:
              ,AVG(sign_ups)  OVER (  ORDER BY date  
                                                        RANGE BETWEEN  6 PRECEDING AND CURRENT ROW)














    1) -------- second highest salary FROM 
    If there is no second highest salary, the query should report null.

    SELECT  distinct salary
    FROM
    (
      SELECT    salary,  dense_rank()  OVER  (Order by salary desc)  as rankn
      FROM employee
    )  as t1 

    WHERE 
      t1.rankn = n


    2) -------- Write an SQL query to find all numbers that appear at least three times consecutively.
    SELECT  l1.num 
    FROM     logs l1
    Inner join logs l2 
          on       l2.id     = l1.id -1 
              and l2.num = l1.num

    Inner Join logs l3
          on           l3.id = l1.id -2 
              and l3.num = l1.num

          ------ Using lag (previous row
    Select num FROM logs 
    FROM logs   
    WHERE  
          num = lag(num,1) 
    and num = lag(num,2) 
    and id - 1 = lag(id,1) 
    and id - 2 = lag(id,2) 




















    3)   --------   Write an SQL query to find the employees who are high earners in each of the departments.
    https:///department-top-three-salaries/submissions/

    WITH topk_employee AS (
        SELECT   
                id, name, salary, departmentID,

                dense_rank() OVER ( PARTITION BY departmentID  order by salary desc    ) as topk_rank
        FROM Employee as t1    
    ) 

    SELECT   t2.name as department
            ,t1.name as Employee
            ,t1.salary as salary
          
    FROM topk_employee as t1

            LEFT JOIN (SELECT id, name FROM Department) as t2
            ON t1.departmentID = t2.id

    WHERE t1.topk_rank <= 3
        



    -------- Median Salary or Quantille Salary  ------------------------------------------------------------------------------------------------
    -- Write your  query statement below

    with median_id as (
        SELECT      *
                      ,row_number() over(partition by company order by salary) as rank1
                      ,count(company) over(partition by company) as cnt

        FROM employee
    )

    SELECT   id, company, salary
    FROM median_id
        WHERE  rank1  between  cnt/2.0 and cnt/2.0 + 1
















    4) ---------- *: Find the month-over-month percentage change for monthly active users (MAU).
      If n_user > 0 :

              WITH user_count AS (
              SELECT tyear, tmonth  count(user_id) as n_user
    FROM  (
      Select   year(date) as tyear, month(date) as tmonth, user_id
      FROM users  )
                ),

    SELECT  tyear, tmonth,  (n_user / lag(n_user,1) -1.0)*100.0   as mau_pct_chg
    FROM  user_count
    group by tyear, tmonth
    ORDER BY tyear ASC, tmonth ASC



    5) **Task:** Write a query that gets the number of retained users per month. In this case, retention for a given month is defined as the number of users who logged in that month who also logged in the immediately previous month.


    WITH monrhtly_user AS
    (
                SELECT tdate   count(user_id) as n_user
    FROM  (
      Select  date(year= year(t1.date), month=month(t1.date), 1)  as tdate, user_id
      FROM users as t1
    )
    group by tdate
    ORDER BY tdate
    
    )
    Select
      year(t1.date), month(t1.year), count(u.user_id) AS n_user
    From monthly_users AS t1
    INNER Join monthly_users AS t2   
      ON   t1.user_id = t2.user_id 
      AND CAST(month(t2.tdate) as INT) = cast(month(DATEADD(month, -1, t1.tdate)) as INT) 
      AND CAST(year(t2.tdate)  as INT) = cast(year(DATEADD(month,  -1, t1.tdate)) as INT)












    6) --------  **Task:** Now we’ll take retention and turn it on its head: Write a query to find how many users last month *did not* come back this month. i.e. the number of churned users. 

    SELECT   tyear, tmonth, count(user_id)
    FROM       users t1                 ------   (Previous month)

    LEFT JOIN users   AS t2       ------   Next month
    ON   
      t2.user_id = t1.user_id
      AND  MONTH( t2.date) =  MONTH( dateadd(month, +1,  t1.date   )
      AND  YEAR(  t2.date)   =  YEAR(   dateadd(month,  +1,    t1.date   )
    WHERE
            t2.user_id IS NULL

    GROUP BY tyear, tmonth

    trick:         LEFT JOIN    t2.user_id is NULL       ===  user_id NOT IN (  Select user_id ...)



    7) **Task: **Write a query to get *cumulative* cash flow for each day such that we end up with a table in the form below: 

    with cf_table AS     (
                --  cashflow per date
    SELECT date, sum(cash_flow) as cf    
    FROM      cash_flows as t1
    GROUP BY date
    ORDER by date
    ),
    SELECT t1.date,  sum(t2.cf) as cumulative_cf  
    FROM cf_table as t1

    INNER JOIN (
          Select   *  FROM cf_table
          )  AS t2 
        ON  t2.date <= t1.date   ----  OK: sum of previous days
    GROUP BY t1.date   
    


    8) **Task**: Write a query to get 7-day rolling (preceding) average of daily sign ups. 

    SELECT 
    t1.date, 
    AVG(t2.sign_ups) average_sign_ups 
    FROM signups AS t1
    INNER JOIN signups AS t2 
          ON   t1.date   >=  dateadd(day, -6, t2.date)  ---- preceding 6 days
          AND  t1.date   <=  t2.date                    ---- that day itself. 
    GROUP BY t1.date






    Using windowing in Hive SQL:
    SELECT date
              ,AVG(sign_ups)  OVER (  ORDER BY date  
                                                      ROWS BETWEEN  6 PRECEDING AND CURRENT ROW) ------ not familiar with this 
              as signup_avg_7day
    FROM table t1

    ------ With Missing days:
              ,AVG(sign_ups)  OVER (  ORDER BY date  
                                                        RANGE BETWEEN  6 PRECEDING AND CURRENT ROW)






    9) ---------- **Task: **Write a query to get the response time per email (`id`) sent to `zach@g.com` . Do not include `id`s that did not receive a response FROM [zach@g.com](mailto:zach@g.com). Assume each email thread has a unique subject. Keep in mind a thread may have multiple responses back-and-forth between [zach@g.com](mailto:zach@g.com) and another email address. 

    SELECT 
    e1.subject, 
    MIN(e2.timestamp) - e1.timestamp as time_to_respond  ------ Most recent one
    FROM emails e1
    INNER JOIN emails e2 ON 
    e2.subject = e1.subject AND 
    e2.FROM    = e1.to      AND 
    e2.to      = e1.FROM    AND 
    e2.timestamp >  e1.timestamp ---- after current email
    WHERE e1.to = 'zach@g.com' 
    GROUP BY e1.subject



    10) ------ **Task**: Write a query to get the `empno` with the highest salary. Make sure your solution can handle ties!

    WITH  salaries_rank (
    SELECT 
    empno, depname, salary,  rank_dense() OVER  (      ORDER  BY salaries DESC  ) as rank
    ------  rank 1,1,1, 2,2,2 on duplicates
    ),

    SELECT empno, depname, salary, rank
    FROM salaries_rank
    WHERE
    rank=1







    11) **Task:** Write a query that returns the same table, but with a new column that has average salary per `depname`. 

    SELECT
    depname, empno. salary,
    ROUND( AVG(salary), 0) OVER (  PARTITION BY depname)
    FROM salaries

    ------ using left JOIN :
    SELECT   t1.depname, t1.empno, t1.salary, t2.avg_salary
    FROM salaries as t1
    LEFT JOIN (
      SELECT depname,  ROUND( AVG( salary), 0) as avg_salary FROM salaries GROUP By depname
    ) as t2
    ON t1.depname = t2.depname



    **Task:** Write a query that adds a column with the rank of each employee based on their salary within their department, 
    SELECT
      depname, empno, salary,
      rank_dense()  OVER (  PARTITION BY depname  ORDER BY salary DESC ) as salary_rank



    12) **Task:** Write a query to count the number of sessions that fall into bands of size 5, i.e. for the above snippet, produce something akin to: 

    ----------  Dynamic Bucket  : Ok Correct
    WITH tbuckets AS (
        SELECT session_id,
                CONCAT(
        CAST( 5*ROUND(length / 5, 0 )        AS STRING),  
        "-",
        CAST( 5*ROUND(length / 5, 0 ) + 5  AS STRING),  
    )    AS bucket
    ,

    SELECT  bucket,  count(session_id) as count1
    FROM tbuckets
    GROUP BY bucket








    13) **Task:** Write a query to get the pairs of states with total streaming amounts within 1000 of each other. For the snippet above, we would want to see something like:

    ------ Cartesian Product,  
    SELECT t1.state as state_a,  t2.state as state_b

    FROM states  AS t1

    LEFT JOIN
    (  SELECT    *  FROM states
    ) AS t2
    ON  
        (           t1.total_streams - t2.streams  <= 1000    ---- Yes 
          AND  t1.total_streams  - t2.streams  >= -1000
          AND  t1.state != t2.state
        )



    13) **Task:** How could you modify the SQL FROM the solution to Part 1 of this question so that duplicates are removed? if we used the sample table FROM Part 1, the pair `NC` and `SC` should only appear in one row 

    ------ Cartesian Product without duplicates  ,
    ------  IF  string comparison  < is accepted
    SELECT 
        CASE 
          WHEN  t1.state < t2.state  THEN     t1.state
          ELSE   t2.state
      END  AS state_a,  

        CASE 
          WHEN  t1.state < t2.state  THEN     t2.state
          ELSE   t1.state
      END   AS   state_b

    FROM states

    LEFT JOIN
    (  SELECT    *  FROM states

    ) AS t2
    ON  
        (           t1.total_streams - t2.streams  <= 1000
          AND  t1.total_streams - t2.streams  >= -1000
          AND  t1.state != t2.state





    **Task:** Assume there are only two possible values for `class`. Write a query to count the number of users in each class such that any user who has label `a` and `b` gets sorted into `b`, any user with just `a` gets sorted into `a` and any user with just `b` gets into `b`. 
    -------- Using Array storage for values (finite, small)
    WITH  t1 AS (
    SELECT  user
      CASE
          WHEN 'a'   = ANY( class_array) AND 'b'  = ANY( class_array)   THEN  'b'
          WHEN 'a'   = ANY( class_array)    THEN  'a'
          WHEN 'b'   = ANY( class_array)    THEN  'b'
          ELSE 'none'
    END  class

    FROM (
    SELECT  user,
        ARRAY_AGG(  class  ) as class_array   ------ Stored all values in ARRAY  < small issue with duplicates....
    FROM users
    GROUP BY user
    )
    ),

    SELECT   class, count(*) as count
    FROM      t1
    GROUP BY  class


    Monthly Percentage Difference

    WITH 
    cte AS (
      SELECT *,
                    CAST( date_format(date, "%Y-%m-01") AS DATE) as dt_month         
    )

    SELECT dt_month
          (sum(value) / lag(sum(value), 1) -1  OVER (ORDER BY dt_month ASC)  as revenue_pct
    FROM cte
    GROUP BY dt_month


    What is the 3-month moving average of the vaccinations in each country
    SELECT date1,
      ROUND(AVG(n_users) OVER(PARTITION BY Country ORDER BY Month 
                                                      ROWS BETWEEN 2 PRECEDING AND CURRENT ROW ),0) 
      AS mv_average
    FROM monthly



    -------- Count NULL 
    SUM(CASE WHEN jobresponses.result = 'true' THEN 1 ELSE 0 END) as True,






    Percent Change in Daily Website Visits
    SELECT   LAG(visits) OVER(PARTITION BY website ORDER BY date) AS previous_day_visits
    FROM daily_visits;






    1-day increase/decrease in total number of visits
    WITH daily_visits_lag AS (
    SELECT  date1
                  ,LAG(visits) OVER(PARTITION BY website ORDER BY date) AS previous_day_visits
      FROM daily_visits
    )
    SELECT date1   
          ,    COALESCE(round((visits//day_visits_prev -1.0)  *100),0) AS percent_change
    FROM daily_visits_la


    Which months registered the lowest vaccinations for each country?
    SELECT *,
      RANK() OVER(PARTITION BY Country ORDER BY num_vaccinations ASC ) as rk
    FROM --Monthly_Vaccinations
    WHERE rk = 1


    ------ Rolling Moving average  in SQL
    SELECT  date,   STDEV(avgnet) 
              OVER (  ORDER BY date    ROWS BETWEEN 10 PRECEDING AND CURRENT ROW   ) AS stddev
    FROM   price


    -------- Pct Rates average   ----------------------------------------------------------------------------------
    WITH trates AS(
      SELECT  date1,
        CAST(SUM(
                        CASE WHEN AVG_TEMP IS NULL THEN 1 ELSE 0 END)
                  AS FLOAT) / COUNT(*) AS AVG_TEMP_NULL_RATE
      FROM  t1 
      GROUP BY  date1
    ),
    trates_AVG AS(
      SELECT  date1,
        AVG(AVG_TEMP_NULL_RATE) OVER (
          ORDER BY DATE_ADDED ASC
          ROWS BETWEEN 14 PRECEDING AND CURRENT ROW) AS 2week_rolling_avg
      FROM trates
      GROUP BY  date1
    )

    SELECT *FROM trates_avg
    WHERE
        AVG_TEMP_NULL_RATE -  2weeks_rolling_avg > 0.3;



















    ______________________________________________________________________________
    https:///average-salary-departments-vs-company/
    Output: 
    +-----------+---------------+------------+
    | pay_month | department_id | comparison |
    +-----------+---------------+------------+
    | 2017-02   | 1             | same       |
    | 2017-03   | 1             | higher     |

    Write an SQL query to report the comparison result (higher/lower/same) of the average salary of employees in a department to the company's average salary.

    -- Write your  query statement below
    WITH   department_salary AS  (
      SELECT department_id
                ,avg(amount) as department_avg
                ,date_format(pay_date, '%Y-%m') as pay_month
      FROM salary 
      LEFT JOIN employee on salary.employee_id = employee.employee_id
      group by department_id, pay_month
    ),

    company_salary  AS (
      SELECT avg(amount) as company_avg,  
                    date_format(pay_date, '%Y-%m') as pay_month 
      FROM salary group 
      by date_format(pay_date, '%Y-%m')
    )

    SELECT  t1.pay_month 
              ,t1.department_id
              ,CASE
      WHEN  department_avg > t2.company_avg  THEN     'higher'
      WHEN  department_avg < t2.company_avg   THEN    'lower'
                  ELSE  'same'
                END AS comparison

    FROM  department_salary as t1
    LEFT JOIN  company_salary as t2
      on  t1.pay_month = t2.pay_month
















    https:///finding-the-topic-of-each-post/
    Write an SQL query to find the topics of each post according to the following rules:

    If the post does not have keywords FROM any topic, its topic should be "Ambiguous!".
    If the post has at least one keyword of any topic, its topic should be a string of the IDs of its topics sorted in ascending order and separated by commas ','. The string should not contain duplicate IDs.


    WITH cte AS (

        SELECT post_id, topic_id
        FROM Posts p
        LEFT JOIN Keywords k
        ON CONCAT(' ', content, ' ') LIKE CONCAT('% ', word, ' %')

    )

    SELECT post_id, 
        COALESCE( GROUP_CONCAT(DISTINCT topic_id
                              ORDER BY topic_id
                              SEPARATOR ','), 
                              'Ambiguous!') AS 'topic'
    FROM  cte t
    GROUP BY post_id



    https:///new-users-daily-count/
    Write an SQL query to reports for every date within at most 90 days FROM today, the number of users that logged in for the first time on that date. Assume today is 2019-06-30.

    +---------+----------+---------------+
    | user_id | activity | activity_date |
    +---------+----------+---------------+
    | 1       | login    | 2019-05-01    |
    | 1       | homepage | 2019-05-01    |

    WITH first_login AS(
    SELECT user_id, MIN(activity_date) AS login_date
    FROM Traffic
    WHERE activity = 'login'
    GROUP BY user_id
    )

    SELECT login_date, COUNT(*) as user_count
    FROM first_login
    WHERE login_date >= DATEADD(day, -90, '2019-06-30')
    GROUP BY login_date








    https:///unpopular-books/

    Write an SQL query that reports the books that have sold less than 10 copies in the last year, excluding books that have been available for less than one month FROM today. Assume today is 2019-06-23.

    Return the result table in any order.
    The query result format is in the following example.


    SELECT 
    b.book_id,
    b.name
    FROM 
    (SELECT * FROM books WHERE  available_FROM <= "2019-05-23") b 
    LEFT JOIN  (SELECT * FROM orders WHERE  dispatch_date >= "2018-06-23") o
    on b.book_id=o.book_id 
    group by b.book_id,b.name
    having sum(o.quantity) is null or sum(quantity)<10




































    https:///first-and-last-call-on-the-same-day/
    +--------------+----------+
    | Column Name  | Type     |
    +--------------+----------+
    | caller_id    | int      |
    | recipient_id | int      |
    | call_time    | datetime |
    +--------------+----------+
    (caller_id, recipient_id, call_time) is the primary key for this table.
    Each row contains information about the time of a phone call between caller_id and recipient_id.
    

    Write an SQL query to report the IDs of the users whose first and last calls on any day were with the same person. Calls are counted regardless of being the caller or the recipient.

    Return the result table in any order.


    with all_Callers as (
    SELECT caller_id user_id, recipient_id as reciever_id  , call_time FROM Calls
    union 
    SELECT recipient_id v, caller_id as  reciever_id ,call_time FROM Calls
    )

    ,first_last_caller as ( 
    select
    distinct user_id ,
    first_value(reciever_id) over (partition by user_id,date(call_time) order by call_time) first_recipient_id,
    first_value(reciever_id) over (partition by user_id,date(call_time) order by  call_time desc) last_recipient_id   
    FROM all_Callers
    )

    SELECT   user_id
    FROM  first_last_caller
    WHERE  
        first_recipient_id = last_recipient_id
    group by user_id








    Write an SQL query to find the total number of users and the total amount spent using the mobile only, the desktop only, and both mobile and desktop together for each date.
    Spending table:
    +---------+------------+----------+--------+
    | user_id | spend_date | platform | amount |
    | 1       | 2019-07-01 | mobile   | 100    |
    | 1       | 2019-07-01 | desktop  | 100    |

    Output: 
    +------------+----------+--------------+-------------+
    | spend_date | platform | total_amount | total_users |
    | 2019-07-01 | desktop  | 100          | 1           |
    | 2019-07-01 | mobile   | 100          | 1           |
    | 2019-07-01 | both     |    0          | 0           |
    Explanation:

    Issue of zero value for some dates

    WITH 
    t1 AS(
    SELECT spend_date, user_id,
          CASE WHEN COUNT(DISTINCT platform) = 2 THEN 'both'
                    ELSE platform END AS platform, 
          SUM(amount) AS amount
    FROM Spending
    GROUP BY spend_date, user_id
    ),

    t2(spend_date, platform) AS(   -- Get all the dates
    SELECT DISTINCT(spend_date), 'desktop'  FROM Spending    UNION
    SELECT DISTINCT(spend_date), 'mobile'   FROM Spending    UNION
    SELECT DISTINCT(spend_date), 'both'     FROM Spending
    )

    SELECT     t2.*, 
                      IFNULL(  SUM(amount), 0)                         AS total_amount,
                      IFNULL(  COUNT( DISTINCT user_id), 0)  AS total_users
    FROM t2
    LEFT JOIN t1
    ON     t2.spend_date = t1.spend_date 
    AND   t2.platform       = t1.platform
    GROUP BY 1, 2














    https:///number-of-transactions-per-visit/

    Visits table:
    | user_id | visit_date |
    | 1       | 2020-01-01 |
    | 2       | 2020-01-02 |
    | 9       | 2020-01-25 |
    | 8       | 2020-01-28 |

    Transactions table:
    | user_id | transaction_date | amount |
    | 1       | 2020-01-02       | 120    |
    | 8       | 2020-01-28       | 1      |
    | 9       | 2020-01-25       | 99     |


    Output: 
    | transactions_count | visits_count |
    | 0                  | 4            |
    | 1                  | 5            |
    | 3                  | 1            |

    Tip: Work backwards to figure out which tables you will ultimately need

    In the final solution you need the following:
    +-------------------+--------------+
    | transactions_count | visits_count |

    +----------+---------------------------+
    | visit_date | num_transactions_by_date |

    +------+----------+-------------------------------------+
    | users | visit_date | num_transactions_by_users_by_date








    WITH 
        -- This is to add 0s to dates when user visite but didn't complete a transaction
        num_transactions_by_users_by_date AS --nvbubd
        (
            SELECT v.user_id
                , visit_date
                , count(transaction_date) AS num_transactions
            FROM visits v
            LEFT JOIN Transactions t        
            ON v.user_id = t.user_id
            AND v.visit_date = t.transaction_date
            -- WHERE  v.user_id in (1,2) -- for testing only
            GROUP BY 1, 2
            ORDER BY 1, 2
        )
        
        , num_transactions_by_date AS --ntbd
        (
            SELECT user_id  -- not really necessary but leaving it in for testing small use case
                ,visit_date
                , sum(num_transactions) AS num_transactions
            FROM num_transactions_by_users_by_date
            -- WHERE  user_id in (1,2)  -- for testing only
            GROUP BY 1,2
            ORDER BY 1,2
        )
        
        -- This is to list the give an ordered list starting FROM 0 up to the max_number_transactions      
        ,num_transactions AS --nt
        (
            SELECT row_number() over () as num_transactions
            FROM transactions
            UNION SELECT 0   
        )
        
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --    
    -- Test CTEs
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --    

    -- SELECT * FROM num_transactions_by_users_by_date
    -- SELECT * FROM num_transactions_by_date
    -- SELECT * FROM num_transactions


    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --    
    -- Max number of calculations
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  

    -- SELECT MAX(num_transactions) FROM num_transactions_by_date

    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --    
    -- Final Query
    -- -- -- -- -- -- -- -- -- -- -- -- -- -- --   

    SELECT nt.num_transactions AS transactions_count
      , COUNT(ntbd.num_transactions) AS visits_count
    FROM num_transactions AS nt
    LEFT JOIN num_transactions_by_date AS ntbd
    ON nt.num_transactions = ntbd.num_transactions
    WHERE nt.num_transactions <= (SELECT MAX(num_transactions) FROM num_transactions_by_date)
    -- AND ntbd.user_id in (1,2) -- for testing only
    GROUP BY 1
    ORDER by 1




    https:///report-contiguous-dates/

    | fail_date         |
    +-------------------+
    | 2018-12-28        |
    | 2018-12-29        |
    | 2019-01-04        |

    | success_date      |
    +-------------------+
    | 2018-12-30        |
    | 2019-01-02        |
    | 2019-01-03        |
    | 2019-01-06        |

    Find Output as :
    | period_state | start_date   | end_date     |
    | succeeded    | 2019-01-01   | 2019-01-03   |
    | failed       | 2019-01-04   | 2019-01-05   |
    | succeeded    | 2019-01-06   | 2019-01-06   |


    ___________________________________________________________________________________
    with main as (
                  SELECT 'failed' as flag,
                            fail_date as date1
                  FROM failed WHERE  fail_date between '2019-01-01' and '2019-12-31'
    union all
    SELECT 'succeeded' as flag,
                success_date as date1 
    FROM succeeded WHERE  success_date between '   2019-01-01' and '2019-12-31'
    ),

    mappings as(
    SELECT *, 
              dense_rank() over (order by date1) - dense_rank() over (partition by flag order by date1) as map1      
    FROM main
    )

    SELECT 
                flag as period_state ,
                min(date1) as start_date,
                max(date1) as end_date
    FROM 
                mappings
    group by flag, map1
    order by start_date





    -- Write an SQL query to find for each month and country: 
    -- the number of approved transactions and their total amount, 
    -- the number of chargebacks, and their total amount.

    !!!! Be careful ChargeBack  and Transaction ARE in different DATE

    WITH t1 AS(
        SELECT  ta.*
              ,date_format(ta.trans_date, "%Y-%m") as dtmonth
              ,'approved' AS state2 
        FROM Transactions as ta
        WHERE ta.state = 'approved'
    )

    ,t2 AS(
        SELECT   ta.*
            ,date_format(tc.trans_date, "%Y-%m") as dtmonth
            ,'charge' AS state2

        FROM Chargebacks as tc
        INNER JOIN  Transactions AS ta on  tc.trans_id = ta.id    
    )

    ,t3 AS (
          SELECT  * FROM t1        UNION ALL
          SELECT  * FROM t2
    )

    SELECT  
          t3.dtmonth as month
        ,t3.country
        
        ,SUM( IF(state2 ='approved', 1, 0 ) )            AS  approved_count
        ,SUM( IF(state2 ='approved', amount, 0 ) )  AS  approved_amount
    
        ,SUM( IF(state2 ='charge', 1, 0 ) )               AS   chargeback_count
        ,SUM( IF(state2 ='charge', amount, 0 ) )     AS   chargeback_amount

    FROM t3
    GROUP BY dtmonth, country
    ORDER BY dtmonth, country









    https:///get-the-second-most-recent-activity/
    Input: 
    UserActivity table:
    +------------+--------------+-------------+-------------+
    | username   | activity     | startDate   | endDate     |
    | Alice      | Travel       | 2020-02-12  | 2020-02-20  |
    | Alice      | Dancing      | 2020-02-21  | 2020-02-23  |
    | Alice      | Travel       | 2020-02-24  | 2020-02-28  |
    | Bob        | Travel       | 2020-02-11  | 2020-02-18  |

    Output: 
    +------------+--------------+-------------+-------------+
    | username   | activity     | startDate   | endDate     |
    | Alice      | Dancing      | 2020-02-21  | 2020-02-23  |
    | Bob        | Travel       | 2020-02-11  | 2020-02-18  |



    SELECT username, activity, startDate, endDate
    FROM (
          SELECT  *
                          ROW_NUMBER() over(partition by username order by startdate desc) n 
                        ,count(activity) over(partition by username)    cnt   --------  In case of 1 activty 

          FROM UserActivity 
    ) AS  t1
    WHERE  n=2 or cnt<2  

    Use window function to calculate the count and order the starting date. 
    And we SELECT either rank = 2 or count = 1 in statement. Pretty nice.

















    Output: 
    +------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Category   | Monday    | Tuesday   | Wednesday | Thursday  | Friday    | Saturday  | Sunday    |
    +------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Book       | 20        | 5         | 0         | 0         | 10        | 0         | 0         |
    | Glasses    | 0         | 0         | 0         | 0         | 5         | 0         | 0         |
    | Phone      | 0         | 0         | 5         | 1         | 0         | 0         | 10        |
    | T-Shirt    | 0         | 0         | 0         | 0         | 0         | 0         | 0         |




    WITH cte AS 
      (
        SELECT i.item_category, WEEKDAY(o.order_date) AS "day", SUM(o.quantity) AS "total"
        FROM Orders o LEFT JOIN Items i ON i.item_id = o.item_id
        GROUP BY 1, 2 ORDER BY 1, 2
      ),
      final AS 
      (
        SELECT i.item_category AS "Category",
        IFNULL(MAX(CASE WHEN c.day = 0 THEN c.total END), 0) AS "Monday",
        IFNULL(MAX(CASE WHEN c.day = 1 THEN c.total END), 0) AS "Tuesday",
        IFNULL(MAX(CASE WHEN c.day = 2 THEN c.total END), 0) AS "Wednesday",
        IFNULL(MAX(CASE WHEN c.day = 3 THEN c.total END), 0) AS "Thursday",
        IFNULL(MAX(CASE WHEN c.day = 4 THEN c.total END), 0) AS "Friday",
        IFNULL(MAX(CASE WHEN c.day = 5 THEN c.total END), 0) AS "Saturday",
        IFNULL(MAX(CASE WHEN c.day = 6 THEN c.total END), 0) AS "Sunday"
        FROM Items i LEFT JOIN cte c ON i.item_category = c.item_category
        GROUP BY 1 ORDER BY 1
      )

      SELECT * FROM final





















    https:///page-recommendations-ii/

    Input:  Friendship table:
    +----------+----------+
    | user1_id | user2_id |
    | 1        | 2        |
    | 2        | 5        |

    Likes table:
    +---------+---------+
    | user_id | page_id |
    | 1       | 88      |
    | 6       | 33      |
    | 6       | 88      |

    Write an SQL query to find all the possible page recommendations for every user. Each recommendation should appear as a row in the result table with these columns:
    Output: 
    +---------+---------+---------------+
    | user_id | page_id | friends_likes |
    | 1       | 77      | 2             |
    | 1       | 23      | 1             |
    | 2       | 24      | 1             |


    __________________________________________________________________________
    -- first, prep a table that contains all users and their friendsselect
    with t1 as (
        SELECT user1_id as user_id, user2_id as friend_id FROM friendship
        union
        SELECT user2_id as user_id, user1_id as friend_id FROM friendship
    )
        
    -- then, join table
    SELECT    t1.user_id
                    ,l.page_id
                    ,count(distinct t1.friend_id) as friends_likes
    FROM t1
    LEFT JOIN  likes as l
    on t1.friend_id=l.user_id

    -- filter out pages that are already liked by the user
    LEFT JOIN  likes as l2
    on       t1.user_id= l2.user_id 
    and     l.page_id = l2.page_id

    WHERE  l2.page_id is null

    group by t1.user_id, l.page_id







    Write an SQL query to report the IDs of the users whose first and last calls on any day were with the same person. Calls are counted regardless of being the caller or the recipient.

    Input: Calls table:
    | caller_id | recipient_id | call_time           |
    | 8         | 4            | 2021-08-24 17:46:07 |
    | 11        | 3            | 2021-08-17 13:07:00 |
    | 8         | 11           | 2021-08-17 22:22:22 |

    Output: 
    | user_id |
    | 1       |
    | 4       |
    | 5       |

    WITH
    call_all AS  (
    SELECT caller_id as user_id, recipient_id, call_time, date_format( call_time, '%Y%m%d')  as dateday 
    FROM Calls
    UNION
    SELECT recipient_id, caller_id, call_time, date_format( call_time, '%Y%m%d')  as dateday  
    FROM    Calls
    )

    ,call_min AS (   select user_id, min(call_time) as call_time_min from call_all
                            group by date(call_time), user_id 
    ) 

    ,call_max AS (  select user_id, max(call_time) as call_time_max from call_all 
                            group by date(call_time), user_id
    ) 

    --------Flatten the table:
    SELECT distinct t1.user_id
    FROM cte as t1
    INNER JOIN  (  SELECT *  FROM cte   
                            WHERE (user_id, call_time) in     ( select user_id, call_time_min from call_min )
    )  AS t2  
    ON t1.user_id = t2.user_id   AND t1.dateday = t2.dateday

    INNER JOIN   (SELECT *  FROM cte   
                            WHERE (user_id, call_time) in     ( select user_id, call_time_max from call_max )
    ) AS t3
    ON t1.user_id = t3.user_id   AND t1.dateday = t3.dateday
                
                -------- Conditions  same recipient, same user, same day.
                AND t2.dateday      = t3.dateday
                AND t2.user_id       = t3.user_id         
                AND t2.recipient_id = t3.recipient_id


    https:///market-analysis-ii/

    Write an SQL query to find for each user whether the brand of the second item (by date) they sold is their favorite brand. If a user sold less than two items, report the answer for that user as no. It is guaranteed that no seller sold more than one item on a day.


    Users table:
    | user_id | join_date  | favorite_brand |
    | 1       | 2019-01-01 | Lenovo         |
    | 2       | 2019-02-09 | Samsung        |
    | 3       | 2019-01-19 | LG             |
    | 4       | 2019-05-21 | HP             |

    Orders table:
    | order_id | order_date | item_id | buyer_id | seller_id |
    | 1        | 2019-08-01 | 4       | 1        | 2         |
    | 2        | 2019-08-02 | 2       | 1        | 3         |
    | 3        | 2019-08-03 | 3       | 2        | 3         |
    | 4        | 2019-08-04 | 1       | 4        | 2         |
    | 5        | 2019-08-04 | 1       | 3        | 4         |
    | 6        | 2019-08-05 | 2       | 2        | 4         |

    Items table:
    | item_id | item_brand |
    | 1       | Samsung    |
    | 2       | Lenovo     |
    | 3       | LG         |
    | 4       | HP         |

    Output: 
    | seller_id | 2nd_item_fav_brand |
    | 1         | no                 |
    | 2         | yes                |
    | 3         | yes                |
    | 4         | no                 |

    1) Flatten the order list with additional info
    list of item by date, per seller_id, per brand name

      join with user fav_brand, item_brand

    buyer_id, seller_id --> user_id

    2) Filter with conditions

    3) Re-format, group by to provide infos.
    pick the 2nd item sold, and returnn









    rank(): 1,2,3,3, 5,6,6,  7,7
    dense_rank(): 1,2,3,4,5,6,7


    WITH
    -- Flatten all table in order
    order_seller_all AS (
      SELECT ta.*
            ,dense_rank() OVER ( PARTITION BY seller_id ORDER BY order_date ASC )  AS rank_item
            , ti.item_brand
      
      FROM orders as ta
      LEFT JOIN items  as ti   ON ta.item_id = ti.item_id
    )

    -- JOIN and reduce
    SELECT  
        t1.user_id as seller_id
        ,CASE 
          WHEN t2.rank_item = 2 AND t2.item_brand = t1.favorite_brand   THEN 'yes'
          ELSE   'no'
        END  2nd_item_fav_brand


    FROM users  as t1   
    
    -- Join with reduce condition 
    LEFT JOIN (  SELECT  *
        FROM order_seller_all
        WHERE rank_item = 2
    ) as t2
        ON  t1.user_id = t2.seller_id























    https:///the-number-of-seniors-and-juniors-to-join-the-company/

    1) Hiring the largest number of seniors.
    2) After hiring the maximum number of seniors, use the remaining budget to hire the largest number of juniors.
    Write an SQL query to find the number of seniors and juniors hired under the mentioned criteria.

    Candidates table:
    +-------------+------------+--------+
    | employee_id | experience | salary |
    | 1           | Junior     | 10000  |
    | 11          | Senior     | 20000  |
    | 13          | Senior     | 50000  |
    | 4           | Junior     | 40000  |

    Output: 
    | experience | accepted_candidates |
    | Senior     | 2                   |
    | Junior     | 2                   |

    the budget is $70000 

    1)select all  senior cumsum  salary from lower to higher
    cumsum < budget    --> Doe NOT work 
        since one senior has over-budget, need to follow with junior.
    order by experience, salary
    2) groupby formatted.


    WITH 
    CTE AS (
        SELECT  *
                      , SUM(salary) OVER(PARTITION BY experience ORDER BY salary,employee_id ASC) 
        AS cumsum FROM Candidates
    )
          
    SELECT 'Senior' AS experience
                  ,COUNT(employee_id) AS accepted_candidates 
    FROM CTE 
            WHERE experience = 'Senior' AND cumsum < 70000

    UNION
    SELECT    'Junior' AS experience
                    ,COUNT(employee_id) AS accepted_candidates 
    FROM CTE 
    WHERE experience = 'Junior' 
                  AND cumsum < (  SELECT 70000 - IFNULL(MAX(cumsum),0) 
                                                FROM CTE WHERE experience = 'Senior' AND cumsum < 70000
                                            )







































    https:///sales-by-day-of-the-week/
    Write an SQL query to report how many units in each category have been ordered on each day of the week.

    table: Orders
    | Column Name   | Type    |
    +---------------+---------+
    | order_id      | int     |
    | customer_id   | int     |
    | order_date    | date    | 
    | item_id       | varchar |
    | quantity      | int     |
    +---------------+---------+
    
    Table: Items
    | Column Name         | Type    |
    +---------------------+---------+
    | item_id             | varchar |
    | item_name           | varchar |
    | item_category       | varchar |

    ------ Output is pivot table
    | Category   | Monday    | Tuesday   | Wednesday | Thursday  | Friday    | Saturday  | Sunday    |
    +------------+-----------+-----------+-----------+-----------+-----------+-----------+-----------+
    | Book       | 20        | 5         | 0         | 0         | 10        | 0         | 0         |
    | Glasses    | 0  


    SELECT
        b.item_category as 'CATEGORY'

    ,sum(case when weekday(a.order_date) = 0 then a.quantity else 0 end) as 'MONDAY',
    sum(case when weekday(a.order_date) = 1 then a.quantity else 0 end) as 'TUESDAY',
    sum(case when weekday(a.order_date) = 2 then a.quantity else 0 end) as 'WEDNESDAY',
    sum(case when weekday(a.order_date) = 3 then a.quantity else 0 end) as 'THURSDAY',
    sum(case when weekday(a.order_date) = 4 then a.quantity else 0 end) as 'FRIDAY',
    sum(case when weekday(a.order_date) = 5 then a.quantity else 0 end) as 'SATURDAY',
    sum(case when weekday(a.order_date) = 6 then a.quantity else 0 end) as 'SUNDAY'

    FROM orders a 
    RIGHT JOIN  items b on a.item_id = b.item_id
    GROUP BY  b.item_category
    ORDER BY  b.item_category












    Input: 
    Stadium table:
    | id   | visit_date | people    |
    | 1    | 2017-01-01 | 10        |
    | 2    | 2017-01-02 | 109       |
    | 3    | 2017-01-03 | 150       |
    | 8    | 2017-01-09 | 188       |


    Output: 
    | id   | visit_date | people    |
    | 5    | 2017-01-05 | 145       |
    | 6    | 2017-01-06 | 1455      |
    | 7    | 2017-01-07 | 199       |


    Write an SQL query to display the records 
    with three or more rows with consecutive id's, and the number of people is greater than or equal to 100 for each.
    Return the result table ordered by visit_date in ascending order.

    WITH
    cte AS (
        SELECT ID
            , visit_date
            , people
            , LEAD(people, 1) OVER (ORDER BY id) nxt
            , LEAD(people, 2) OVER (ORDER BY id) nxt2
            , LAG(people, 1) OVER (ORDER BY id) pre
            , LAG(people, 2) OVER (ORDER BY id) pre2
        FROM Stadium
    )


    SELECT ID
        , visit_date
        , people
    FROM cte 
    WHERE (cte.people >= 100 AND cte.nxt >= 100 AND cte.nxt2 >= 100) 
        OR (cte.people >= 100 AND cte.nxt >= 100 AND cte.pre >= 100)  
        OR (cte.people >= 100 AND cte.pre >= 100 AND cte.pre2 >= 100)























    https:///page-recommendations-ii/

    Friendship table:
    +----------+----------+
    | user1_id | user2_id |
    | 1        | 2        |
    | 2        | 5        |
    | 6        | 1        |

    Likes table:
    +---------+---------+
    | user_id | page_id |
    | 1       | 88      |
    | 2       | 23      |

    | 3       | 77      |
    | 6       | 88      |

    Output: 
    +---------+---------+---------------+
    | user_id | page_id | friends_likes |
    | 1       | 77      | 2             |
    | 5       | 77      | 1             |
    | 5       | 23      | 1             |
    Your system will recommended a page to user_id if the page is liked by 
    at least one friend of user_id and is not liked by user_id.


    -- first, prep a table that contains all users and their friends
    with t1 as (
        select user1_id as user_id, user2_id as friend_id from friendship
        union
        select user2_id as user_id, user1_id as friend_id from friendship)
        
    -- then, join table
    select t1.user_id, l.page_id, count(distinct t1.friend_id) as friends_likes
    from t1
    left join likes as l
    on t1.friend_id=l.user_id

    -- filter out pages that are already liked by the user
    left join likes as l2
    on t1.user_id=l2.user_id and l.page_id=l2.page_id
    where l2.page_id is null

    -- get the final output
    group by t1.user_id, l.page_id


    New 2:

    find the number of sessions completed by users that had their very first session as viewers.  You should just return their user ID and number of sessions.

    ---------- Solution by YAKI
    WITH  tresult AS (
    Select user_id , count( Distinct session_id)  AS n_sessions
    GROUP BY user_id
    ),

    WITH session_rank AS (

      SELECT   user_id, session_type             
                        ---- rank_dense() :same rank is possible...
                        RANK_DENSE() OVER (    PARTITION BY  user_id    
                                                                    ORDER BY  session_start ASC ) as rank
      -- ------ No need GROUP BY user_id, session_type  because of partition BY

    )

    SELECT  t1.user_id, t1.n_sessions
    FROM  tresult  AS t1

    INNER JOIN (  -- Select only the one wanted

      SELECT *  FROM session_rank
      WHERE
          rank = 1 AND  session_type='viewer'

    ) AS t2   ON   t1.user_id  =  t2.user_id










    ----------  Solution by Yaki
    calculate the rating from the second latest film and the average lifetime rating for each one of the actors and movies they acted in. Output a list of actors, their rating from the second latest film, the average lifetime rating and the difference between the two ratings (second last - average).”


    WITH avg_rating_per_actor AS (

      SELECT name, AVG(rating)      AS avg_rating
      FROM movies          
    ),

    WITH rating_per_actor AS (

      SELECT name,
                      amg_movie_id,  rating,                
                    RANK_DENSE() OVER ( PARTITION by name  ORDER BY name DESC, year DESC, amg_movie_id DESC  ) AS rank

                    ------ WHY not using   row_number() ???? row_number is indexing through all rows, while rank is indexing with partition by actor
    Good point !!

      FROM movies

    )



    SELECT  t1.rating             AS  second_last_rating,
                    t2.avg_rating     AS .lifetime_rating,   
                    t1.rating -  t2.avg_rating AS  variance

    FROM  rating_per_actor as T1

    LEFT JOIN (
      SELECT   * FROM   avg_rating_per_actor 

    ) AS t2  ON   t1.name = t2.name

    WHERE
      t1.rank=2

















    615 Average Salary: Departments VS Company

    Given two tables as below, write a query to display the comparison result (higher/lower/same) of the average salary of employees in a department to the company's average salary.



    ------------ Solution by Yaki
    WITH  company AS (
      SELECT  AVG(salary) as avg_salary  FROM salary
    ),


    WITH  salary_month AS (
        SELECT  t1.employee,  date(t1.pay_date, 'month') as month, AVG(salary) as avg_salary  FROM salary
        GROUP BY t1.employee_id, t1.month
    ),


    WITH  department AS (
        SELECT  t2.department_id,   date(t1.pay-date, 'month ') as pay_month,    AVG(salary) as avg_salary  
        FROM salary_month  as t1
        LEFT JOIN ( SELECT * FROM Employee) as t2 on t2.employee_id = t1.employee_id
        GROUP BY t2.department_id, t1.month
    ),


    SELECT    
      t1.pay_month,  t1.department_id,
      CASE 
          WHEN   t1.avg_salary > t2.avg_salary  THEN 'higher'
          WHEN   t1.avg_salary = t2.avg_salary  THEN 'same'
          WHEN   t1.avg_salary < t2.avg_salary  THEN 'lower'
          ELSE  NULL





















    579)  The __Employee__ table holds the salary information in a year.
    Write a SQL to get the cumulative sum of an employee's salary over a period of 3 months but exclude the most recent month.
    The result should be displayed by 'Id' ascending, and then by 'Month' descending.




    -------- Book solution:
    A) -- MySQL: single join
    SELECT
      e1.Id
      ,MAX(e2.Month) AS Month
      ,SUM(e2.Salary) AS Salary
    FROM Employee e1
    JOIN Employee e2
      ON e1.Id = e2.Id
      AND e1.Month - e2.Month BETWEEN 1 AND 3
    GROUP BY e1.Id, e1.Month
    ORDER BY e1.Id ASC, e1.Month DESC








    Write an SQL query to display the records with three or more rows with consecutive id's, and the number of people is greater than or equal to 100 for each.
    Return the result table ordered by visit_date in ascending order.



    select distinct day1.* 
    from 
    stadium day1, stadium day2, stadium day3
    where 
    day1.people >= 100 and day2.people >= 100 
    and day3.people >= 100 and
    ((day1.id + 1 =  day2.id and day1.id + 2 = day3.id) or 
    (day1.id - 1 = day2.id and day1.id + 1 = day3.id) or 
    (day1.id - 2 = day2.id and day1.id - 1 = day3.id)) 
    order by day1.id; 












    --1. Classes More Than 5 Students @ LeetCode
    There is a table courses with columns: student and class. Please list out all classes which have more than or equal to 5 students. For example, the table:

    +---------+------------+
    | student | class      |
    +---------+------------+
    | A       | Math       |
    | B       | English    |
    | C       | Math       |
    | D       | Biology    |
    | E       | Math       |
    | F       | Computer   |
    | G       | Math       |
    | H       | Math       |
    | I       | Math       |
    +---------+------------+
    Should output:
    +---------+
    | class   |
    +---------+
    | Math    |
    +---------+


    -------- Duplicate in each course.
    -- Write your  query statement below
    SELECT class 
    FROM courses
    GROUP BY class
    HAVING COUNT(DISTINCT student)>=5














    _____________________________________________________________________________

    Write a SQL query that reports the device that is first logged in for each player.

    The query result format is in the following example:

    Activity table:
    +-----------+-----------+------------+--------------+
    | player_id | device_id | event_date | games_played |
    +-----------+-----------+------------+--------------+
    | 1         | 2         | 2016-03-01 | 5            |
    | 1         | 2         | 2016-05-02 | 6            |
    | 2         | 3         | 2017-06-25 | 1            |
    | 3         | 1         | 2016-03-02 | 0            |
    | 3         | 4         | 2018-07-03 | 5            |
    +-----------+-----------+------------+--------------+
    Result table:
    +-----------+-----------+
    | player_id | device_id |
    +-----------+-----------+
    | 1         | 2         |
    | 2         | 3         |
    | 3         | 1         |
    +-----------+-----------+
    https:///game-play-analysis-ii/



    --3. Sellers With No Sales @ LeetCode

    Write an SQL query to report the names of all sellers who did not make any sales in 2020. Return the result table ordered by seller_name in ascending order. The query result format is in the following example.

    https:///sellers-with-no-sales/

















    https:///active-users/submissions/
    Active users are those who logged in to their accounts for five or more consecutive days.
    Write an SQL query to find the id and the name of active users.

    ---------- Gap Island problem :  consecutive days.
    SELECT DISTINCT a.id, t2.name

    FROM logins a

    INNER JOIN logins b  
        ON  a.id = b.id 
        AND DATEDIFF(a.login_date, b.login_date) BETWEEN 1 AND 4

    LEFT JOIN Accounts as t2   ON a.id = t2.id

    GROUP BY a.id,  a.login_date
    HAVING COUNT(DISTINCT b.login_date) = 4



    _______________________________________________________
    with 
    logins2 AS (
      SELECT DISTINCT t1.*
            ,t2.name
            , CAST( DATE_FORMAT(t1.login_date, "%Y%m%d"  ) AS DATE ) AS dateday
      from logins as t1
        
      LEFT JOIN accounts AS t2 ON t1.id = t2.id  

    )

    SELECT distinct t1.id, t1.name
    FROM logins2 as t1

    INNER JOIN logins2 as t2 
      ON    t1.id = t2.id
        AND  datediff(t1.dateday, t2.dateday )= 1  

    INNER JOIN logins2 as t3
      ON    t1.id = t3.id
        AND  datediff(t1.dateday, t3.dateday )= 2

    INNER JOIN logins2 as t4
      ON    t1.id = t4.id
        AND  datediff(t1.dateday, t4.dateday )= 3

    INNER JOIN logins2 as t5
      ON    t1.id = t5.id
        AND  datediff(t1.dateday, t5.dateday )= 4

    ORDER BY id ASC



    ---------- Gap Island problem :  consecutive days. add ob 
    with temp0 AS
    (SELECT  id,
                login_date,
                dense_rank() OVER(PARTITION BY id ORDER BY login_date) as row_num
        FROM Logins),

    consective_days as (
        select id, login_date, row_num,
            DATE_ADD(login_date, INTERVAL -row_num DAY) as Groupings
        from temp0),

    answer_table as (SELECT  id,
            MIN(login_date) as startDate,
            MAX(login_date) as EndDate,
            row_num,
            Groupings, 
            count(id),
            datediff(MAX(login_date), MIN(login_date)) as duration
    FROM temp1
    GROUP BY id, Groupings
    HAVING datediff(MAX(login_date), MIN(login_date)) >= 4
    ORDER BY id, StartDate)
    
    select distinct a.id, name
    from answer_table a
    join Accounts acc on acc.id = a.id
    order by a.id''
























    https:///products-with-three-or-more-orders-in-two-consecutive-years/submissions/

    Write an SQL query to report the IDs of all the products that were ordered three or more times
    in two consecutive years.

    WITH cte as(
      SELECT  product_id, 
          year(purchase_date) AS dt_year
    FROM orders
    GROUP BY dt_year, product_id
    HAVING COUNT(order_id) >= 3   -- Conditions
    )
    
    SELECT DISTINCT c1.product_id 
    FROM cte c1 
    INNER JOIN cte c2
        ON   c2.product_id =  c1.product_id 
        AND  c2.dt_year     =  c1.dt_year - 1


    /* Scalable Solution */
    with purchases_per_year as (
        select    product_id 
                ,YEAR(purchase_date)  as purchase_year 
                ,count( order_id) number_of_purchases

        from orders
        group by product_id, YEAR(purchase_date) 
        having count(order_id ) >=3
    )

    ,t2 AS (
    select  product_id

        --- if same consecutive year, keep same group value = start of Consecutive year
      ,purchase_year + 1 - rank() over (partition by product_id order by purchase_year) rank_group 
    from purchases_per_year
    )

    select distinct product_id
    from t2

    group by product_id, rank_group
    having count(rank_group) >=2
    rank_group : GROUP OF consecutive year.  In same group, same consecutive year







    ------ Previous day check

    Write an SQL query to report the IDs of the users that made any two purchases at most 7 days apart.
    Return the result table ordered by user_id.

      Window and LAG die to   t1.purchase_id <. t2.purchase_id   ------in Self JOIN

    WITH cte AS (

      select   user_id, 
                  purchase_date,
                  lag(purchase_date) over (partition by user_id order by purchase_date) prev_purchase_date
      from purchases
    )

    select  distinct user_id
    from  cte
    where datediff(purchase_date, prev_purchase_date) <=7









    Write an SQL query to find for each month and country: the number of approved transactions and their total amount, the number of chargebacks, and their total amount.

    WITH t1 AS (
        SELECT LEFT(chargebacks.trans_date, 7) AS dtmonth, country, 
          "back" AS state, amount
          FROM chargebacks
          INNER JOIN transactions ON chargebacks.trans_id = transactions.id
    UNION ALL
        SELECT LEFT(trans_date, 7) AS month, country, state, amount
          FROM transactions
          WHERE state = "approved"
    )

    SELECT dtmonth, country, 
          SUM(CASE WHEN state = "approved" THEN 1 ELSE 0 END) AS approved_count 
          ,SUM(CASE WHEN state = "approved" THEN amount ELSE 0 END) AS approved_amount
          ,SUM(CASE WHEN state = "back" THEN 1 ELSE 0 END) AS chargeback_count
          ,SUM(CASE WHEN state = "back" THEN amount ELSE 0 END) AS chargeback_amount
    FROM t1
    GROUP BY dtmonth, country
    --318 ms




    Write an SQL query that reports the books that have sold less than 10 copies in the last year, excluding books that have been available for less than one month from today. Assume today is 2019-06-23.

    WITH
    t1 AS (
    SELECT  book_id, sum(quantity) as book_sold
    from Orders 
        where dispatch_date between '2018-06-23' and '2019-06-23'
        group by book_id
    )

    SELECT b.book_id, b.name
    FROM  books b
    left join t1
          on b.book_id = t1.book_id

    WHERE    available_from < '2019-05-23'
                    and (book_sold is null or book_sold <10)
    order by b.book_id


    Write an SQL query that selects the product id, year, quantity, and price for the first year of every product sold.
    WITH
    t1 AS (
    SELECT ta.*
                  ,tb.product_name
                , dense_rank() OVER ( PARTITION BY product_id  ORDER BY year ASC )  AS rank1
    FROM Sales as ta

    LEFT JOIN Product as tb
        ON ta.product_id = tb.product_id
    )

    select  product_id, year as first_year, quantity, price
    FROM t1
    WHERE   rank1 = 1










    Write an SQL query to find all the people who viewed more than one article on the same date.

    WITH
    -- Cnt Unique views per user
    t1 AS ( 
          SELECT    viewer_id
                ,view_date 
                ,count(distinct article_id) as cnt
        FROM Views 
        GROUP BY viewer_id, view_date
    )

    ,t2 AS (
        -- >1 article on (view_date, viwerer_id )
        SELECT  viewer_id, view_date 
        FROM t1
        WHERE  t1.cnt > 1
    )


    SELECT distinct viewer_id as id
    from t2
    ORDER BY id ASC































    --  A bank account is suspicious if the total income exceeds the max_income for this account 
    --   for two or more consecutive months. 
    --   The total income of an account in some month is the sum of all its deposits
    --   in that month (i.e., transactions of the type 'Creditor').

    WITH
    t1 AS(
        SELECT account_id
            ,CASE 
                WHEN type = 'Creditor'  THEN +amount
                WHEN type = 'Debtor'    THEN 0     -- zero in that case
                ELSE  0
              END amt
                  , CAST( date_format(day, '%Y-%m-01')  AS DATE) AS dtmonth
        FROM Transactions
    )

    ,t2 AS (
        SELECT account_id
              ,dtmonth
              ,sum(amt) as amt           
        FROM t1
        GROUP BY account_id, dtmonth
    )


    ,t3 AS(
      SELECT  ta.account_id
        FROM Accounts as ta
        
        INNER JOIN t2
        ON ta.account_id = t2.account_id
        
        INNER JOIN t2 as t2b
        ON      t2.account_id = t2b.account_id
            AND datediff(t2.dtmonth, t2b.dtmonth) < 32
            AND t2.dtmonth > t2b.dtmonth

        WHERE
            t2.amt > ta.max_income
        AND  t2b.amt > ta.max_income 

    )

    SELECT distinct account_id
    FROM t3
    ORDER By account_id ASC







    -- rank without hole, same scores --> same ranking.
    SELECT score
          ,dense_rank() OVER (  ORDER BY score DESC ) AS `rank`
    FROM Scores






    Write an SQL query to find for each user, the join date and the number of orders they made as a buyer in 2019.

    WITH 
    t1 AS (
      SELECT  buyer_id
            ,count(item_id) AS n_order
            ,YEAR(order_date) as dtyear
      FROM ORDERS
      GROUP BY buyer_id,   YEAR(order_date)     
    )

    SELECT 
        ta.user_id as buyer_id
        ,ta.join_date
        ,IFNULL( tb.n_order, 0) AS orders_in_2019
        
    FROM Users as ta

        LEFT JOIN  (
          SELECT  * FROM t1
          WHERE t1.dtyear = 2019
        ) AS tb
        ON ta.user_id = tb.buyer_id




















    Write an SQL query to find the average daily percentage of posts that got removed after being reported as spam, rounded to 2 decimal places.

    WITH
    t1 AS (
        SELECT post_id
              ,action_date
              ,user_id
        FROM Actions
        WHERE action ='report' AND extra = 'spam'
    )

    ,t2 AS (
        SELECT
        
          t1.action_date
          ,SUM(CASE WHEN tb.remove_date is NULL THEN 0 ELSE 1 END ) / COUNT( distinct t1.post_id) as pct_post_removed
            
        FROM t1    
        LEFT JOIN Removals AS tb
                    ON tb.post_id = t1.post_id

        GROUP BY t1.action_date
    )

    SELECT  ROUND( AVG(pct_post_removed) * 100, 2) as average_daily_percent
    FROM t2

    ------ Edge case of duplicate t1.post_id





















    ------ Pre-Defined table Use UNION !!!
    Write an SQL query to report the number of experiments done on each of the three platforms for each of the three given experiments. Notice that all the pairs of (platform, experiment) should be included in the output including the pairs with zero experiments.

    WITH 
    all_platform (platform) AS (
        SELECT 'Android' FROM  Experiments  UNION
        SELECT 'IOS' FROM  Experiments      UNION 
        SELECT 'Web' FROM Experiments
    )

    ,all_experiment (experiment_name) AS (
        SELECT  'Reading' FROM Experiments     UNION
        SELECT 'Programming' FROM Experiments  UNION
        SELECT'Sports' FROM Experiments
    )

    ,A AS (SELECT    platform, experiment_name
    FROM all_platform CROSS JOIN all_experiment
    )

    ,B AS (SELECT  platform, experiment_name, COUNT(*) num_experiments
    FROM Experiments 
    GROUP BY platform, experiment_name
    )

    SELECT
        A.platform,
        A.experiment_name,
        IFNULL(num_experiments,0) AS num_experiments
    FROM  A

    LEFT JOIN B
        ON  A.platform = B.platform 
      AND  A.experiment_name = B.experiment_name

    ORDER BY A.platform, A.experiment_name
















    Write an SQL query to reports for every date within at most 90 days from today, the number of users that logged in for the first time on that date. Assume today is 2019-06-30.

    WITH
    t0 AS (  SELECT user_id,  activity_date
      FROM Traffic 
      WHERE activity ='login'  
    )

    ,t1 AS (
      SELECT  user_id
              ,activity_date          
              ,dense_rank() OVER ( PARTITION BY user_id ORDER BY activity_date ) AS rank1
      FROM t0
    )

    SELECT activity_date AS login_date
          ,count(distinct user_id) AS user_count
    FROM t1
    WHERE
                  -- Condition on 1st log
                  t1.rank1=1
                  AND datediff('2019-06-30', activity_date) <= 90

    GROUP BY activity_date




























    Write an SQL query to report the number of bank accounts of each salary category. The salary categories are:

    WITH 
    t1(category) AS(
    SELECT 'Low Salary' FROM Accounts  UNION
    SELECT 'Average Salary' FROM Accounts  UNION
    SELECT 'High Salary' FROM Accounts 
    )

    ,t2 AS (
    SELECT account_id    
        ,CASE
          WHEN income < 20000 THEN 'Low Salary'
          WHEN income >= 20000  AND income <= 50000 THEN 'Average Salary'
          WHEN income > 50000 THEN 'High Salary'
          ELSE NULL   
        END category
    FROM Accounts
    )


    SELECT   t1.category
                    ,IFNULL( count(t2.category), 0) AS accounts_count

    FROM   t1
    LEFT JOIN t2 ON t1.category = t2.category
    GROUP BY t1.category




    Write an SQL query to report the IDs of the users that made any two purchases at most 7 days apart.
    WITH
    t1 AS (
      SELECT  ta.user_id
      FROM purchases as ta  
      INNER JOIN purchases as tb
        ON ta.user_id = tb.user_id
          AND datediff(ta.purchase_date , tb.purchase_date) <=7 
          AND ta.purchase_date >= tb.purchase_date   
          AND ta.purchase_id <> tb.purchase_id
      
      WHERE     tb.purchase_date is not NULL    AND ta.purchase_date is not NULL
    )

    SELECT distinct user_id
    FROM t1
    ORDER BY user_id ASC






    Write an SQL query to find the total number of users and the total amount spent using the mobile only, the desktop only, and both mobile and desktop together for each date.


    WITH
    tboth AS(
      SELECT ta.user_id, ta.spend_date
      FROM Spending  as ta
        INNER JOIN Spending as tb
        ON  ta.user_id = tb.user_id
            AND ta.platform <> tb.platform
            AND ta.platform is not NULL
            AND tb.platform is not NULL          
            AND ta.spend_date = tb.spend_date

    GROUP BY ta.spend_date      
    )


    ,tmd AS (
      SELECT  tx.spend_date
              ,'both' as platform
              ,count(distinct tx.user_id) as total_users    
              ,sum(tx.amount)             as total_amount
      FROM Spending  as tx
        WHERE
            (user_id, spend_date) IN ( SELECT * FROM tboth)
      GROUP BY tx.spend_date   
    )


    ,tm AS (
      SELECT  tx.spend_date
              ,'mobile' as platform
              ,count(tx.user_id) as total_users    
              ,sum(tx.amount)    as total_amount
      FROM Spending  AS tx
      WHERE tx.platform ='mobile' 
            AND (user_id, spend_date) NOT IN ( SELECT * FROM tboth)
      GROUP BY tx.spend_date   
    )


    ,td AS (
      SELECT  tx.spend_date
              ,'desktop' as platform
              ,count(tx.user_id) as total_users    
              ,sum(tx.amount)    as total_amount
      FROM Spending  AS tx
      WHERE tx.platform ='desktop' 
        AND (user_id, spend_date) NOT IN ( SELECT * FROM tboth)
      GROUP BY tx.spend_date   
    )


    ,tlabel(spend_date, platform) AS (
    SELECT spend_date, 'desktop' FROm Spending UNION
    SELECT spend_date, 'mobile' FROm Spending UNION
    SELECT spend_date, 'both' FROm Spending 
    )


    SELECT t0.spend_date, t0.platform
          ,IFNULL(total_amount, 0) AS total_amount
          ,IFNULL(total_users, 0)  AS total_users 
    FROM tlabel as t0
    LEFT JOIN tmd ON  t0.spend_date = tmd.spend_date AND t0.platform = tmd.platform
    WHERE t0.platform ='both'


    UNION
    SELECT t0.spend_date, t0.platform
          ,IFNULL(total_amount, 0) AS total_amount
          ,IFNULL(total_users, 0)  AS total_users 
    FROM tlabel as t0
    LEFT JOIN tm ON  t0.spend_date = tm.spend_date AND t0.platform = tm.platform
    WHERE t0.platform ='mobile'


    UNION
    SELECT t0.spend_date, t0.platform
          ,IFNULL(total_amount, 0) AS total_amount
          ,IFNULL(total_users, 0)  AS total_users 
    FROM tlabel as t0
    LEFT JOIN td ON  t0.spend_date = td.spend_date AND t0.platform = td.platform

    WHERE t0.platform ='desktop'



























    The cumulative salary summary for an employee can be calculated as follows:
    For each month that the employee worked, sum up the salaries in that month and the previous two months. This is their 3-month sum for that month. If an employee did not work for the company in previous months, their effective salary for those months is 0.
    Do not include the 3-month sum for the most recent month that the employee worked for in the summary.
    Do not include the 3-month sum for any month the employee did not work.


    WITH
    t1 AS (
      SELECT    id, month
          , SUM(salary) OVER (PARTITION BY id  ORDER BY  month 
                            RANGE BETWEEN 2 PRECEDING AND CURRENT ROW    ) as 3mth_salary

      FROM Employee  
    )
    -- Exclude most recent
    ,t2 AS (
      SELECT id, max(month) as month_max
      FROM Employee  
      GROUP BY id 
    )

    SELECT  id , month
                  ,3mth_salary AS salary        
    FROM t1
    WHERE   (id, month) NOT In (SELECT * FROM t2)
    ORDER BY id ASC,  month DESC
























    Median of
      number, freq
    --   Partition into separate parts.
    --   Rank =count(total)/2 --. median
    --   Count total = sume(frequency)
    --   Cumulative rank and rank < 1


    WITH 
    t1 as (
      SELECT  
            num,     
            SUM(frequency) OVER (ORDER BY NUM ASC) as cum_freq
      FROM Numbers  
      ORDER BY num ASC       
    )

    ,t2 AS (
                SELECT sum(frequency)  as n_freq FROM Numbers 
    )

    ,t3 AS (    
        SELECT min(cum_freq) as cum_freq_min
        FROM t1, t2
        WHERE     t1.cum_freq  >= t2.n_freq/2.0     
    )

    ,t3b AS (
        SELECT min(cum_freq) as cum_freq_min    
        FROM t1, t2
        WHERE     t1.cum_freq  >= t2.n_freq/2.0 + 1
    )

    SELECT AVG(t1.num) as  median
    FROM  t1, t3, t3b
    WHERE t1.cum_freq   =  t3.cum_freq_min
              OR t1.cum_freq =  t3b.cum_freq_min

    --------

    where 
    (Mod(a.tot, 2) = 1 and b.cum - f < (a.tot+1)/2 and b.cum >= (a.tot+1)/2)
    or
    (Mod(a.tot, 2) = 0 and 
    ((b.cum - f < a.tot/2 and b.cum >= a.tot/2)
    or
    (b.cum - f < a.tot/2 + 1 and b.cum >= a.tot/2 + 1)





    -- Write your MySQL query statement below

      -- 5 days consective
      
      -- Pattern
      --  Self join or window  for  date coniditions
      --   Flatten attribute
      --  Aggregate and pick columns
        
    -- Write your MySQL query statement below

      -- 5 days consective login
      Pattern
      --  Self join or window  for  date coniditions
      --  Aggregate and pick columns
      --   Flatten attribute
        
      WITH
      t0 AS (
          SELECT distinct ta.id, ta.login_date       
          FROM Logins as ta           
      )
      
      ,t1 AS (
          SELECT ta.id
                ,ta.login_date       
                ,dense_rank() OVER (PARTITION BY ta.id   ORDER BY login_date DESC
                                    ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
                                  ) AS rank1
          FROM t0 AS ta
      )
      
    SELECT t1.id, tc.name
    FROM t1

    LEFT JOIN Accounts AS tc    ON t1.id = tc.id

    -- 4 last log dates
    LEFT JOIN (
      SELECT * FROM t1 WHERE rank1 = 4
    ) AS  tb
      ON  t1.id = tb.id 
      
    WHERE 
      -- Consesutive days
      datediff( t1.login_date, tb.login_date) = 4








    ------ CHURN %
    https:///active-users/
    current not  current mont but previous
    t2 AS (
    SELECT  t1.id

    FROM   t1    -- in T-1

    LEFT JOIN t1  as t2  -- in T 
      ON  t2.id = t1.id
      AND  datediff(t1.login_date,  t2.login_date  ) = -1
      AND t2.is NULL
    )

    SELECT count(t2.id)  / count(t1.id)   
    FROM t2, t1




































    WITH
    monthly_usage AS (
        SELECT 
          user_id, 
          datediff(month, '1970-01-01', dt_timestamp) AS dtmonth
        FROM events
        WHERE event = 'login' GROUP BY user_id, dtmonth order by user_id,dtmonth
    ),
    
    lag_lead AS (  -- Previous Active Month, Next Active month.
        SELECT user_id, dtmonth,
          lag(dtmonth,1)  over (partition by user_id order by user_id, dtmonth)
          ,lead(dtmonth,1) over (partition by user_id order by user_id, dtmonth)
        FROM monthly_usage
    )
    
    ,lag_lead_with_diffs AS (
        SELECT user_id, dtmonth, 
          lag,lead 
          ,dtmonth-lag  AS lag_size      -- Last time active
          ,lead-dtmonth AS lead_size   -- Next time active
        FROM lag_lead
    )
    

    ,calculated AS (
        SELECT dtmonth,

          CASE when lag is null  then  'NEW'
            when lag_size = 1 then       'ACTIVE'     -- Previous month
            when lag_size > 1 then        'RETURN'   -- Far Past
          END AS this_month_state
        
          ,CASE when (lead_size > 1 OR lead_size IS NULL) then 'CHURN'
            else NULL
          END AS next_month_churn
        
          ,count(distinct user_id)  AS n_unique_users

        FROM lag_lead_with_diffs
        GROUP BY dtmonth, this_month_state, next_month_churn
    )
    

    SELECT dtmonth, this_month_state, sum(count) 
      FROM calculated GROUP BY dtmonth,this_month_state

    UNION

    SELECT  dtmonth+1, 'CHURN', count 
      FROM  calculated 
      WHERE next_month_churn is not null
    order by dtmonth

    PAST Active users in continuous days

    -------- Solution 2 Disctint days
    SELECT DISTINCT t1.id
                  ,tb.name
    FROM logins t1

    LEFT JOIN Accounts AS tb ON  t1.id = tb.id

    LEFT JOIN logins AS t2
    ON   t1.id = t2.id 
        AND DATEDIFF(t1.login_date, t2.login_date) BETWEEN 1 AND 4
    GROUP BY t1.id, t1.login_date
    -- Distinct days in total
    HAVING COUNT(DISTINCT t2.login_date) = 4

    -------- Solution 1 naive
      WITH
      t1 AS (
          SELECT ta.id, ta.login_date
          FROM Logins as ta
          
          INNER JOIN Logins as ta1 
            ON   ta.id = ta1.id              AND  datediff( ta.login_date, ta1.login_date) = 1 
          
          INNER JOIN Logins as ta2 
            ON   ta1.id = ta2.id             AND  datediff( ta1.login_date, ta2.login_date) = 1 

          INNER JOIN Logins as ta3 
            ON   ta2.id = ta3.id             AND  datediff( ta2.login_date, ta3.login_date) = 1 

          INNER JOIN Logins as ta4
            ON   ta3.id = ta4.id             AND  datediff( ta3.login_date, ta4.login_date) = 1 
      )
      
      SELECT  distinct t1.id, t2.name
      FROM t1
      LEFT JOIN Accounts AS t2    ON t1.id = t2.id
      ORDER BY id ASC






    -------- CHURN RATE
    {"headers":{"Accounts":["id","name"],"Logins":["id","login_date"]},"rows":{"Accounts":[[1,"Winston"],[7,"Jonathan"]],"Logins":[[7,"2020-05-30"],[1,"2020-05-30"],[7,"2020-05-31"],[7,"2020-06-01"],[7,"2020-06-02"],[7,"2020-06-02"],[7,"2020-06-03"],[1,"2020-06-07"],[7,"2020-06-10"],[7,"2020-07-10"]]}}

    WITH 
    t1 AS ( 
      SELECT   *
                      ,CAST( date_format(login_date, "%Y-%m-01")  AS DATE) as dtmonth                
      FROM  Logins  
    )

    ,tchurn AS(
        SELECT    tpast.dtmonth 
                        ,count( distinct tpast.id )
        
        FROM  t1 as tpast        
        LEFT JOIN t1 AS tnow      
            ON    tnow.id = tpast.id
            AND DATE_ADD(tnow.dtmonth,  INTERVAL -1 MONTH ) = tpast.dtmonth
        
        WHERE        tnow.id IS NULL    
        GROUP BY  tpast.dtmonth
    )


    ,treturn AS(
        SELECT    tnow.dtmonth 
                        ,count( distinct tpast.id )
        
        FROM  t1 as tnow        
        LEFT JOIN t1 AS tpast      
            ON    tnow.id = tpast.id
            AND DATE_ADD(tnow.dtmonth,  INTERVAL -1 MONTH ) = tpast.dtmonth
        
        WHERE        tpast.id IS NULL    
        GROUP BY  tnow.dtmonth
    )





    -- Write your MySQL query statement below
    WITH 
    t1 AS (
        SELECT  ta.dept_name
                        ,count(tb.student_id) as student_number

        FROM Department AS ta
        LEFT JOIN Student as tb    ------ NULL exist
                      ON ta.dept_id = tb.dept_id
        GROUP BY ta.dept_name           
    )

    SELECT dept_name
                  ,student_number   
    FROM t1
    ORDER BY student_number DESC, dept_name ASC

    Write an SQL query to report the IDs of all the products that were ordered three or more times in two consecutive years.


    WITH  
    t1 AS(
      SELECT *, YEAR(purchase_date) as tyear from Orders
    ) 

    ,t2 AS (
    SELECT    t1.product_id,   t1.tyear
                    ,count( distinct t2.order_id ) AS n_order_2y
      
    FROM t1
    LEFT JOIN t1 AS t2    -- Rolling Window
      ON
            t1.product_id = t2.product_id
        AND  t2.tyear >= t1.tyear - 1      
        AND  t2.tyear <= t1.tyear      
    GROUP BY  t1.product_id, t1.tyear
    )

    SELECT distinct product_id
    FROM t2 
    WHERE n_order_2y >= 3


    {"headers": {"Orders": ["order_id", "product_id", "quantity", "purchase_date"]}, "rows": {"Orders": [[1, 1, 7, "2020-03-16"], [2, 1, 4, "2020-12-02"], [3, 1, 7, "2020-05-10"], [4, 1, 6, "2021-12-23"], [5, 1, 5, "2021-05-21"], [6, 1, 6, "2021-10-11"], [7, 2, 6, "2022-10-11"], [8, 2, 6, "2022-11-11"], [9, 2, 6, "2023-12-11"], [10, 2, 6, "2024-12-11"]]}}























    Add team_id based on salary

    WITH
    t1 AS (   SELECT salary, count(distinct employee_id ) as n_user    
      FROM Employees
      GROUP BY salary  )

    ,tok AS (
      SELECT * 
        FROM Employees 
        WHERE salary NOT IN ( SELECT salary  FROM t1 WHERE n_user=1 )
    )


    ,t3 AS (
      SELECT   employee_id ,name  ,salary 
          ,dense_rank() OVER( ORDER BY salary ASC) as team_id    
      FROM  tok    
      ORDER BY team_id ASC, employee_id ASC  
    )
    SELECT * FROM t3




    ------ Imbalanced order 
    WITH
    t1 AS (  SELECT 
        order_id
        ,max(quantity) as max_qty
        ,sum(quantity) / count(distinct product_id) as avg_qty
      FROM OrdersDetails    
      GROUP BY order_id    
    )

    ,t2 AS (  SELECT order_id
      FROM  t1
      WHERE  max_qty > (SELECT max(avg_qty) FROM t1 )    
    )
    SELECT order_id FROM t2













    Sequence

    WITH 
    RECURSIVE seq AS (
        SELECT 0 AS value UNION ALL SELECT value + 1 FROM seq WHERE value < 100 
    )

    SELECT * FROM seq;

    -------- Generate 
    WITH 
    tdates AS (
      WITH   t19 AS (
              SELECT  0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union 
              select 7     union select 8 union select 9 )    
      SELECT  adddate('1970-01-01',t4.i*10000 + t3.i*1000 + t2.i*100 + t1.i*10 + t0.i) datei 
      FROM  t19 AS t0, t19 AS t1, t19 AS t2, t19 AS t3,  t19 AS t4 
    )

    select * from tdates
    where datei between '2012-02-10' and '2012-02-15'

















"""




