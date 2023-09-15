import { Controller, Get, Post, Query, Render, UploadedFile, UseInterceptors } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { AppService } from './app.service';
import { ParsingOptions } from 'xlsx';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  @Render('index')
  root(): void {}


  @Post()
  @UseInterceptors(FileInterceptor('file'))
  convert(@UploadedFile() file: Express.Multer.File, @Query() options: ParsingOptions) {
    return this.appService.convert(file, options);
  }
}
