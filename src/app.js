import express from "express";
import cors from "cors";
import morgan from "morgan";
import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";
import { options } from "./swaggerOptions";
import tasksRoutes from "./routes/tasks";

const app = express();

const specs = swaggerJsdoc(options);
//app.set("port", 3000);
app.use(cors());    //toda app puede conectarse a mi servidor
app.use(morgan("dev")); //para ver las peticiones que se hacen
app.use(express.json()); //para que pueda leer los json
app.use(tasksRoutes)

app.use('/docs', swaggerUi.serve, swaggerUi.setup(specs));

export default app;