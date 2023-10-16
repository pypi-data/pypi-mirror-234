# Welcome to Alpha environment documention

Alpha is an **ecosystem** based on a multiple **frameworks** and **libraries** for both **frontend** and **backend**.

## Purpose

The purpose of the **ecosystem** is to simplify any dev activity. 

- Database queries are simpliified:

??? info "Standard query way"

    ```py
    from flask import Flask, request
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
    db = SQLAlchemy(app)

    def get_logs(start_date=None, end_date=None, useLimit=False, pageForLimit=1):
        total = 0
        logs = []
        limit = 20
        start = (pageForLimit - 1) * limit

        query = "SELECT COUNT(*) AS count FROM logs"
        parameters = []
        if start_date is not None and end_date is not None:
            query += " AND CAST(date AS DATE) between %s and %s"
            parameters.append(start_date)
            parameters.append(end_date)       
        query+= " ORDER BY date DESC"

        rows = db.get(query, parameters)
        for row in rows:
            total = row[0]

        query = "SELECT type, origin, message, stack, date FROM logs"
        parameters = []
        if start_date is not None and end_date is not None:
            query += " AND CAST(date AS DATE) between %s and %s"
            parameters.append(start_date)
            parameters.append(end_date)       
        query+= " ORDER BY date DESC"
        if useLimit:
            query+= " LIMIT %s OFFSET %s"
            parameters.append(limit)
            parameters.append(start)

        rows = db.get(query, parameters)        
        for row in rows:
            log = {}
            log["type"] = row[0]
            log["origin"] = row[1]
            log["message"] = row[2]
            log["stack"] = row[3]
            log["date"] = row[4]
            logs.append(log)

        return {'total' : total, 'logs' : logs}
    ```

??? info "FlaskSqlAlchemy way"

    ```py
    from flask import Flask, request
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
    db = SQLAlchemy(app)

    class Log(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        type = db.Column(db.String(50))
        origin = db.Column(db.String(50))
        message = db.Column(db.String(255))
        stack = db.Column(db.String(255))
        date = db.Column(db.DateTime)

    def get_logs():
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        use_limit = request.args.get('use_limit')
        page_for_limit = request.args.get('page_for_limit', default=1, type=int)

        total = 0
        logs = []
        limit = 20
        start = (page_for_limit - 1) * limit

        query = db.session.query(db.func.count(Log.id)).filter(Log.date.between(start_date, end_date))
        if start_date and end_date:
            query = query.filter(db.cast(Log.date, db.Date) >= start_date, db.cast(Log.date, db.Date) <= end_date)
        total = query.scalar()

        query = Log.query.filter(Log.date.between(start_date, end_date)).order_by(Log.date.desc())
        if start_date and end_date:
            query = query.filter(db.cast(Log.date, db.Date) >= start_date, db.cast(Log.date, db.Date) <= end_date)
        if use_limit:
            query = query.limit(limit).offset(start)

        rows = query.all()
        for row in rows:
            log = {
                'type': row.type,
                'origin': row.origin,
                'message': row.message,
                'stack': row.stack,
                'date': row.date
            }
            logs.append(log)

        return {'total': total, 'logs': logs}
    ```

??? tip "Alpha query way"

    ```py
    from core import core
    DB = core.DB

    class Log(DB.Model):
        id = db.Column(db.Integer, primary_key=True)
        type = db.Column(db.String(50))
        origin = db.Column(db.String(50))
        message = db.Column(db.String(255))
        stack = db.Column(db.String(255))
        date = db.Column(db.DateTime)

    
    def get_logs(
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = False,
        page: int = 0,
        per_page: int = 100,
    ):
        return DB.select(
            Logs,
            optional_filters=[
                {Logs.update_date: {">": start_date}},
                {Logs.update_date: {"<": end_date}},
            ],
            page=page,
            per_page=per_page,
            limit=limit,
            order_by=Logs.update_date.desc(),
        )
    ```

??? info "SpringBoot query way"

    ```java
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    import org.springframework.data.jpa.repository.JpaRepository;
    import org.springframework.data.jpa.repository.Query;
    import org.springframework.data.repository.query.Param;
    import org.springframework.web.bind.annotation.GetMapping;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RequestParam;
    import org.springframework.web.bind.annotation.RestController;

    import javax.persistence.Entity;
    import javax.persistence.GeneratedValue;
    import javax.persistence.GenerationType;
    import javax.persistence.Id;
    import javax.persistence.Table;
    import java.time.LocalDate;
    import java.util.List;

    @Entity
    @Table(name = "logs")
    class Log {

        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        private String type;
        private String origin;
        private String message;
        private String stack;
        private LocalDate date;

        // Getters and setters
    }

    interface LogRepository extends JpaRepository<Log, Long> {

        @Query("SELECT COUNT(l) FROM Log l WHERE CAST(l.date AS date) BETWEEN :startDate AND :endDate")
        Long countByDateRange(@Param("startDate") LocalDate startDate, @Param("endDate") LocalDate endDate);

        @Query("SELECT l FROM Log l WHERE CAST(l.date AS date) BETWEEN :startDate AND :endDate ORDER BY l.date DESC")
        List<Log> findByDateRange(@Param("startDate") LocalDate startDate, @Param("endDate") LocalDate endDate);
    }

    class LogController {

        @Autowired
        private LogRepository logRepository;

        @GetMapping
        public ResponseData getLogs(
                @RequestParam(required = false) LocalDate start_date,
                @RequestParam(required = false) LocalDate end_date,
                @RequestParam(required = false, defaultValue = "false") boolean use_limit,
                @RequestParam(required = false, defaultValue = "1") int page_for_limit
        ) {
            long total = 0;
            List<Log> logs;
            int limit = 20;
            int start = (page_for_limit - 1) * limit;

            if (start_date != null && end_date != null) {
                total = logRepository.countByDateRange(start_date, end_date);
            } else {
                total = logRepository.count();
            }

            if (start_date != null && end_date != null) {
                logs = logRepository.findByDateRange(start_date, end_date);
            } else {
                logs = logRepository.findAll();
            }

            if (use_limit) {
                logs = logRepository.findByDateRangeWithLimit(start_date, end_date, limit, start);
            }

            return new ResponseData(total, logs);
        }
    }

    class ResponseData {
        private long total;
        private List<Log> logs;

        public ResponseData(long total, List<Log> logs) {
            this.total = total;
            this.logs = logs;
        }

        // Getters and setters
    }

    @SpringBootApplication
    public class Application {

        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    }    
    ```

- Api route definition are also simplified:

??? info "Classic Flask approch"

    ```py
    from flask import Flask, request
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
    db = SQLAlchemy(app)

    class MyModel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        my_integer = db.Column(db.Integer)
        my_string = db.Column(db.String(100))
        my_floats = db.Column(db.ARRAY(db.Float))

    @app.route('/my_route/<int:my_integer>/<string:my_string>/<float_list>', methods=['GET'])
    def my_route(my_integer, my_string, float_list):
        if my_integer >= 100:
            return 'L\'entier doit être inférieur à 100.', 400

        try:
            float_list = [float(num) for num in float_list.split(',')]
        except ValueError:
            return 'La liste doit contenir uniquement des nombres à virgule flottante.', 400

        results = MyModel.query.filter_by(my_integer=my_integer, my_string=my_string, my_floats=float_list).all()

        return 'Résultats : ' + str(results)

    if __name__ == '__main__':
        app.run()
    ```

??? tip "Alpha approach"

    ```py
    from alphaz.utils.api import route
    from core import core

    app = core.api

    class MyModel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        my_integer = db.Column(db.Integer)
        my_string = db.Column(db.String(100))
        my_floats = db.Column(db.ARRAY(db.Float))

    @route('/my_route', parameters=[
        Parameter('my_integer', ptype=int), 
        Parameter('my_string'), 
        Parameter('float_list', ptype=list[float])
    ], methods=['GET'])
    def my_route():
        results = MyModel.query.filter_by(my_integer=my_integer, my_string=my_string, my_floats=float_list).all()
        return 'Résultats : ' + str(results)

    if __name__ == '__main__':
        core.api.run()
    ```

??? info "SpringBoot approach"

    ```java 
    import javax.persistence.*;

    @Entity
    @Table(name = "my_table")
    public class MyEntity {

        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        private Integer myInteger;

        private String myString;

        @ElementCollection
        private List<Double> myFloats;

        // Getters and setters
    }

    import org.springframework.data.jpa.repository.JpaRepository;

    public interface MyEntityRepository extends JpaRepository<MyEntity, Long> {
    }

    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.util.StringUtils;
    import org.springframework.web.bind.annotation.*;

    import java.util.List;

    @RestController
    @RequestMapping("/my_route")
    public class MyController {

        @Autowired
        private MyEntityRepository myEntityRepository;

        @GetMapping("/{myInteger}/{myString}/{floatList}")
        public ResponseEntity<String> myRoute(
                @PathVariable Integer myInteger,
                @PathVariable String myString,
                @PathVariable List<Double> floatList
        ) {
            if (myInteger >= 100) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("L'entier doit être inférieur à 100.");
            }

            if (floatList.stream().anyMatch(f -> f == null)) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("La liste doit contenir uniquement des nombres à virgule flottante.");
            }

            List<MyEntity> results = myEntityRepository.findByMyIntegerAndMyStringAndMyFloats(myInteger, myString, floatList);

            return ResponseEntity.ok("Résultats : " + results.toString());
        }
    }

    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;

    @SpringBootApplication
    public class MyApplication {

        public static void main(String[] args) {
            SpringApplication.run(MyApplication.class, args);
        }
    }
    ```

## Backend: Alphaz

- Alphaz is a backend toolbox/framework based on a combination between Flask, SqlAlchemy and a multitude of other libraries.

    !!! note
        The overriding goal for Alphaz is to ease the backend development and easely link python backend to Angular frontend [Alphaa].

## Features

-   API Routing parameters management upgrade
-   Enhanced json files configuration

## Tech

Alphaz uses a number of open source projects to work properly:

-   [Flask](https://flask.palletsprojects.com/en/1.1.x/) - a micro web framework
-   [SqlAlchemy](https://www.sqlalchemy.org/) - a database toolkit
-   [Flask-SqlAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - an extension for Flask that adds support for SQLAlchemy

## Project layout

- How to setup `Alpha`: [Alpha](alpha_setup.md)
## Frontend: Alphaa

- Alphaa is a frontend toolbox/framework

    !!! note
        The overriding goal for Alphaa is to ease the frontend development and easely link Angular frontend to python backend [Alphaz].
## Features

- Enhanced services
- Master class


## Project layout

- How to setup `Alpha`: [Alpha](alpha_setup.md)