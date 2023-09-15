import { Injectable } from '@nestjs/common';
import { read, ParsingOptions} from 'xlsx';

@Injectable()
export class AppService {
  convert(file: Express.Multer.File, options: ParsingOptions): object {
    return read(file.buffer, options).Sheets;
  }
}
