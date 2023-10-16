#include <Python.h>
#include <structmember.h>

typedef signed long int GLintptr;
typedef signed long int GLsizeiptr;
typedef unsigned int GLenum;
typedef float GLfloat;
typedef int GLint;
typedef int GLsizei;
typedef unsigned long long GLuint64;
typedef unsigned int GLbitfield;
typedef unsigned int GLuint;
typedef unsigned char GLboolean;
typedef unsigned char GLubyte;
typedef char GLchar;
typedef void * GLsync;

extern void webgl2_glCullFace(GLenum mode);
extern void webgl2_glClear(GLbitfield mask);
extern void webgl2_glTexParameteri(GLenum target, GLenum pname, GLint param);
extern void webgl2_glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const void *pixels);
extern void webgl2_glDepthMask(GLboolean flag);
extern void webgl2_glDisable(GLenum cap);
extern void webgl2_glEnable(GLenum cap);
extern void webgl2_glFlush();
extern void webgl2_glDepthFunc(GLenum func);
extern void webgl2_glReadBuffer(GLenum src);
extern void webgl2_glReadPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, void *pixels);
extern GLenum webgl2_glGetError();
extern void webgl2_glGetIntegerv(GLenum pname, GLint *data);
extern void webgl2_glViewport(GLint x, GLint y, GLsizei width, GLsizei height);
extern void webgl2_glTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const void *pixels);
extern void webgl2_glBindTexture(GLenum target, GLuint texture);
extern void webgl2_glDeleteTextures(GLsizei n, const GLuint *textures);
extern void webgl2_glGenTextures(GLsizei n, GLuint *textures);
extern void webgl2_glTexImage3D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLenum format, GLenum type, const void *pixels);
extern void webgl2_glTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const void *pixels);
extern void webgl2_glActiveTexture(GLenum texture);
extern void webgl2_glBlendFuncSeparate(GLenum sfactorRGB, GLenum dfactorRGB, GLenum sfactorAlpha, GLenum dfactorAlpha);
extern void webgl2_glGenQueries(GLsizei n, GLuint *ids);
extern void webgl2_glBeginQuery(GLenum target, GLuint id);
extern void webgl2_glEndQuery(GLenum target);
extern void webgl2_glGetQueryObjectuiv(GLuint id, GLenum pname, GLuint *params);
extern void webgl2_glBindBuffer(GLenum target, GLuint buffer);
extern void webgl2_glDeleteBuffers(GLsizei n, const GLuint *buffers);
extern void webgl2_glGenBuffers(GLsizei n, GLuint *buffers);
extern void webgl2_glBufferData(GLenum target, GLsizeiptr size, const void *data, GLenum usage);
extern void webgl2_glBufferSubData(GLenum target, GLintptr offset, GLsizeiptr size, const void *data);
extern GLboolean webgl2_glUnmapBuffer(GLenum target);
extern void webgl2_glBlendEquationSeparate(GLenum modeRGB, GLenum modeAlpha);
extern void webgl2_glDrawBuffers(GLsizei n, const GLenum *bufs);
extern void webgl2_glStencilOpSeparate(GLenum face, GLenum sfail, GLenum dpfail, GLenum dppass);
extern void webgl2_glStencilFuncSeparate(GLenum face, GLenum func, GLint ref, GLuint mask);
extern void webgl2_glStencilMaskSeparate(GLenum face, GLuint mask);
extern void webgl2_glAttachShader(GLuint program, GLuint shader);
extern void webgl2_glCompileShader(GLuint shader);
extern GLuint webgl2_glCreateProgram();
extern GLuint webgl2_glCreateShader(GLenum type);
extern void webgl2_glDeleteProgram(GLuint program);
extern void webgl2_glDeleteShader(GLuint shader);
extern void webgl2_glEnableVertexAttribArray(GLuint index);
extern void webgl2_glGetActiveAttrib(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLint *size, GLenum *type, GLchar *name);
extern void webgl2_glGetActiveUniform(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLint *size, GLenum *type, GLchar *name);
extern GLint webgl2_glGetAttribLocation(GLuint program, const GLchar *name);
extern void webgl2_glGetProgramiv(GLuint program, GLenum pname, GLint *params);
extern void webgl2_glGetProgramInfoLog(GLuint program, GLsizei bufSize, GLsizei *length, GLchar *infoLog);
extern void webgl2_glGetShaderiv(GLuint shader, GLenum pname, GLint *params);
extern void webgl2_glGetShaderInfoLog(GLuint shader, GLsizei bufSize, GLsizei *length, GLchar *infoLog);
extern GLint webgl2_glGetUniformLocation(GLuint program, const GLchar *name);
extern void webgl2_glLinkProgram(GLuint program);
extern void webgl2_glShaderSource(GLuint shader, GLsizei count, const GLchar *const*string, const GLint *length);
extern void webgl2_glUseProgram(GLuint program);
extern void webgl2_glUniform1i(GLint location, GLint v0);
extern void webgl2_glUniform1fv(GLint location, GLsizei count, const GLfloat *value);
extern void webgl2_glUniform2fv(GLint location, GLsizei count, const GLfloat *value);
extern void webgl2_glUniform3fv(GLint location, GLsizei count, const GLfloat *value);
extern void webgl2_glUniform4fv(GLint location, GLsizei count, const GLfloat *value);
extern void webgl2_glUniform1iv(GLint location, GLsizei count, const GLint *value);
extern void webgl2_glUniform2iv(GLint location, GLsizei count, const GLint *value);
extern void webgl2_glUniform3iv(GLint location, GLsizei count, const GLint *value);
extern void webgl2_glUniform4iv(GLint location, GLsizei count, const GLint *value);
extern void webgl2_glUniformMatrix2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glVertexAttribPointer(GLuint index, GLint size, GLenum type, GLboolean normalized, GLsizei stride, const void *pointer);
extern void webgl2_glUniformMatrix2x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix3x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix2x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix4x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix3x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glUniformMatrix4x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value);
extern void webgl2_glBindBufferRange(GLenum target, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size);
extern void webgl2_glVertexAttribIPointer(GLuint index, GLint size, GLenum type, GLsizei stride, const void *pointer);
extern void webgl2_glUniform1uiv(GLint location, GLsizei count, const GLuint *value);
extern void webgl2_glUniform2uiv(GLint location, GLsizei count, const GLuint *value);
extern void webgl2_glUniform3uiv(GLint location, GLsizei count, const GLuint *value);
extern void webgl2_glUniform4uiv(GLint location, GLsizei count, const GLuint *value);
extern void webgl2_glClearBufferiv(GLenum buffer, GLint drawbuffer, const GLint *value);
extern void webgl2_glClearBufferuiv(GLenum buffer, GLint drawbuffer, const GLuint *value);
extern void webgl2_glClearBufferfv(GLenum buffer, GLint drawbuffer, const GLfloat *value);
extern void webgl2_glClearBufferfi(GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil);
extern void webgl2_glBindRenderbuffer(GLenum target, GLuint renderbuffer);
extern void webgl2_glDeleteRenderbuffers(GLsizei n, const GLuint *renderbuffers);
extern void webgl2_glGenRenderbuffers(GLsizei n, GLuint *renderbuffers);
extern void webgl2_glBindFramebuffer(GLenum target, GLuint framebuffer);
extern void webgl2_glDeleteFramebuffers(GLsizei n, const GLuint *framebuffers);
extern void webgl2_glGenFramebuffers(GLsizei n, GLuint *framebuffers);
extern void webgl2_glFramebufferTexture2D(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level);
extern void webgl2_glFramebufferRenderbuffer(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer);
extern void webgl2_glGenerateMipmap(GLenum target);
extern void webgl2_glBlitFramebuffer(GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter);
extern void webgl2_glRenderbufferStorageMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height);
extern void webgl2_glFramebufferTextureLayer(GLenum target, GLenum attachment, GLuint texture, GLint level, GLint layer);
extern void *webgl2_glMapBufferRange(GLenum target, GLintptr offset, GLsizeiptr length, GLbitfield access);
extern void webgl2_glBindVertexArray(GLuint array);
extern void webgl2_glDeleteVertexArrays(GLsizei n, const GLuint *arrays);
extern void webgl2_glGenVertexArrays(GLsizei n, GLuint *arrays);
extern void webgl2_glDrawArraysInstanced(GLenum mode, GLint first, GLsizei count, GLsizei instancecount);
extern void webgl2_glDrawElementsInstanced(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount);
extern GLuint webgl2_glGetUniformBlockIndex(GLuint program, const GLchar *uniformBlockName);
extern void webgl2_glGetActiveUniformBlockiv(GLuint program, GLuint uniformBlockIndex, GLenum pname, GLint *params);
extern void webgl2_glGetActiveUniformBlockName(GLuint program, GLuint uniformBlockIndex, GLsizei bufSize, GLsizei *length, GLchar *uniformBlockName);
extern void webgl2_glUniformBlockBinding(GLuint program, GLuint uniformBlockIndex, GLuint uniformBlockBinding);
extern GLsync webgl2_glFenceSync(GLenum condition, GLbitfield flags);
extern void webgl2_glDeleteSync(GLsync sync);
extern GLenum webgl2_glClientWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout);
extern void webgl2_glGenSamplers(GLsizei count, GLuint *samplers);
extern void webgl2_glDeleteSamplers(GLsizei count, const GLuint *samplers);
extern void webgl2_glBindSampler(GLuint unit, GLuint sampler);
extern void webgl2_glSamplerParameteri(GLuint sampler, GLenum pname, GLint param);
extern void webgl2_glSamplerParameterf(GLuint sampler, GLenum pname, GLfloat param);
extern void webgl2_glVertexAttribDivisor(GLuint index, GLuint divisor);

void impl_glCullFace(GLenum mode) {
    webgl2_glCullFace(mode);
}

void impl_glClear(GLbitfield mask) {
    webgl2_glClear(mask);
}

void impl_glTexParameteri(GLenum target, GLenum pname, GLint param) {
    webgl2_glTexParameteri(target, pname, param);
}

void impl_glTexImage2D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLint border, GLenum format, GLenum type, const void *pixels) {
    webgl2_glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels);
}

void impl_glDepthMask(GLboolean flag) {
    webgl2_glDepthMask(flag);
}

void impl_glDisable(GLenum cap) {
    webgl2_glDisable(cap);
}

void impl_glEnable(GLenum cap) {
    webgl2_glEnable(cap);
}

void impl_glFlush() {
    webgl2_glFlush();
}

void impl_glDepthFunc(GLenum func) {
    webgl2_glDepthFunc(func);
}

void impl_glReadBuffer(GLenum src) {
    webgl2_glReadBuffer(src);
}

void impl_glReadPixels(GLint x, GLint y, GLsizei width, GLsizei height, GLenum format, GLenum type, void *pixels) {
    webgl2_glReadPixels(x, y, width, height, format, type, pixels);
}

GLenum impl_glGetError() {
    return webgl2_glGetError();
}

void impl_glGetIntegerv(GLenum pname, GLint *data) {
    webgl2_glGetIntegerv(pname, data);
}

const GLubyte *impl_glGetString(GLenum name) {
    switch (name) {
        case 0x1F00: return (GLubyte *)"WebKit";
        case 0x1F01: return (GLubyte *)"WebKit WebGL";
        case 0x1F02: return (GLubyte *)"WebGL 2.0 (OpenGL ES 3.0)";
        case 0x8B8C: return (GLubyte *)"WebGL GLSL ES 3.00 (OpenGL ES GLSL ES 3.0)";
    }
    return NULL;
}

void impl_glViewport(GLint x, GLint y, GLsizei width, GLsizei height) {
    webgl2_glViewport(x, y, width, height);
}

void impl_glTexSubImage2D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLsizei width, GLsizei height, GLenum format, GLenum type, const void *pixels) {
    webgl2_glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels);
}

void impl_glBindTexture(GLenum target, GLuint texture) {
    webgl2_glBindTexture(target, texture);
}

void impl_glDeleteTextures(GLsizei n, const GLuint *textures) {
    webgl2_glDeleteTextures(n, textures);
}

void impl_glGenTextures(GLsizei n, GLuint *textures) {
    webgl2_glGenTextures(n, textures);
}

void impl_glTexImage3D(GLenum target, GLint level, GLint internalformat, GLsizei width, GLsizei height, GLsizei depth, GLint border, GLenum format, GLenum type, const void *pixels) {
    webgl2_glTexImage3D(target, level, internalformat, width, height, depth, border, format, type, pixels);
}

void impl_glTexSubImage3D(GLenum target, GLint level, GLint xoffset, GLint yoffset, GLint zoffset, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, const void *pixels) {
    webgl2_glTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels);
}

void impl_glActiveTexture(GLenum texture) {
    webgl2_glActiveTexture(texture);
}

void impl_glBlendFuncSeparate(GLenum sfactorRGB, GLenum dfactorRGB, GLenum sfactorAlpha, GLenum dfactorAlpha) {
    webgl2_glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha);
}

void impl_glGenQueries(GLsizei n, GLuint *ids) {
    webgl2_glGenQueries(n, ids);
}

void impl_glBeginQuery(GLenum target, GLuint id) {
    webgl2_glBeginQuery(target, id);
}

void impl_glEndQuery(GLenum target) {
    webgl2_glEndQuery(target);
}

void impl_glGetQueryObjectuiv(GLuint id, GLenum pname, GLuint *params) {
    webgl2_glGetQueryObjectuiv(id, pname, params);
}

void impl_glBindBuffer(GLenum target, GLuint buffer) {
    webgl2_glBindBuffer(target, buffer);
}

void impl_glDeleteBuffers(GLsizei n, const GLuint *buffers) {
    webgl2_glDeleteBuffers(n, buffers);
}

void impl_glGenBuffers(GLsizei n, GLuint *buffers) {
    webgl2_glGenBuffers(n, buffers);
}

void impl_glBufferData(GLenum target, GLsizeiptr size, const void *data, GLenum usage) {
    webgl2_glBufferData(target, size, data, usage);
}

void impl_glBufferSubData(GLenum target, GLintptr offset, GLsizeiptr size, const void *data) {
    webgl2_glBufferSubData(target, offset, size, data);
}

GLboolean impl_glUnmapBuffer(GLenum target) {
    return webgl2_glUnmapBuffer(target);
}

void impl_glBlendEquationSeparate(GLenum modeRGB, GLenum modeAlpha) {
    webgl2_glBlendEquationSeparate(modeRGB, modeAlpha);
}

void impl_glDrawBuffers(GLsizei n, const GLenum *bufs) {
    webgl2_glDrawBuffers(n, bufs);
}

void impl_glStencilOpSeparate(GLenum face, GLenum sfail, GLenum dpfail, GLenum dppass) {
    webgl2_glStencilOpSeparate(face, sfail, dpfail, dppass);
}

void impl_glStencilFuncSeparate(GLenum face, GLenum func, GLint ref, GLuint mask) {
    webgl2_glStencilFuncSeparate(face, func, ref, mask);
}

void impl_glStencilMaskSeparate(GLenum face, GLuint mask) {
    webgl2_glStencilMaskSeparate(face, mask);
}

void impl_glAttachShader(GLuint program, GLuint shader) {
    webgl2_glAttachShader(program, shader);
}

void impl_glCompileShader(GLuint shader) {
    webgl2_glCompileShader(shader);
}

GLuint impl_glCreateProgram() {
    return webgl2_glCreateProgram();
}

GLuint impl_glCreateShader(GLenum type) {
    return webgl2_glCreateShader(type);
}

void impl_glDeleteProgram(GLuint program) {
    webgl2_glDeleteProgram(program);
}

void impl_glDeleteShader(GLuint shader) {
    webgl2_glDeleteShader(shader);
}

void impl_glEnableVertexAttribArray(GLuint index) {
    webgl2_glEnableVertexAttribArray(index);
}

void impl_glGetActiveAttrib(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLint *size, GLenum *type, GLchar *name) {
    webgl2_glGetActiveAttrib(program, index, bufSize, length, size, type, name);
}

void impl_glGetActiveUniform(GLuint program, GLuint index, GLsizei bufSize, GLsizei *length, GLint *size, GLenum *type, GLchar *name) {
    webgl2_glGetActiveUniform(program, index, bufSize, length, size, type, name);
}

GLint impl_glGetAttribLocation(GLuint program, const GLchar *name) {
    return webgl2_glGetAttribLocation(program, name);
}

void impl_glGetProgramiv(GLuint program, GLenum pname, GLint *params) {
    webgl2_glGetProgramiv(program, pname, params);
}

void impl_glGetProgramInfoLog(GLuint program, GLsizei bufSize, GLsizei *length, GLchar *infoLog) {
    webgl2_glGetProgramInfoLog(program, bufSize, length, infoLog);
}

void impl_glGetShaderiv(GLuint shader, GLenum pname, GLint *params) {
    webgl2_glGetShaderiv(shader, pname, params);
}

void impl_glGetShaderInfoLog(GLuint shader, GLsizei bufSize, GLsizei *length, GLchar *infoLog) {
    webgl2_glGetShaderInfoLog(shader, bufSize, length, infoLog);
}

GLint impl_glGetUniformLocation(GLuint program, const GLchar *name) {
    return webgl2_glGetUniformLocation(program, name);
}

void impl_glLinkProgram(GLuint program) {
    webgl2_glLinkProgram(program);
}

void impl_glShaderSource(GLuint shader, GLsizei count, const GLchar *const*string, const GLint *length) {
    webgl2_glShaderSource(shader, count, string, length);
}

void impl_glUseProgram(GLuint program) {
    webgl2_glUseProgram(program);
}

void impl_glUniform1i(GLint location, GLint v0) {
    webgl2_glUniform1i(location, v0);
}

void impl_glUniform1fv(GLint location, GLsizei count, const GLfloat *value) {
    webgl2_glUniform1fv(location, count, value);
}

void impl_glUniform2fv(GLint location, GLsizei count, const GLfloat *value) {
    webgl2_glUniform2fv(location, count, value);
}

void impl_glUniform3fv(GLint location, GLsizei count, const GLfloat *value) {
    webgl2_glUniform3fv(location, count, value);
}

void impl_glUniform4fv(GLint location, GLsizei count, const GLfloat *value) {
    webgl2_glUniform4fv(location, count, value);
}

void impl_glUniform1iv(GLint location, GLsizei count, const GLint *value) {
    webgl2_glUniform1iv(location, count, value);
}

void impl_glUniform2iv(GLint location, GLsizei count, const GLint *value) {
    webgl2_glUniform2iv(location, count, value);
}

void impl_glUniform3iv(GLint location, GLsizei count, const GLint *value) {
    webgl2_glUniform3iv(location, count, value);
}

void impl_glUniform4iv(GLint location, GLsizei count, const GLint *value) {
    webgl2_glUniform4iv(location, count, value);
}

void impl_glUniformMatrix2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix2fv(location, count, transpose, value);
}

void impl_glUniformMatrix3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix3fv(location, count, transpose, value);
}

void impl_glUniformMatrix4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix4fv(location, count, transpose, value);
}

void impl_glVertexAttribPointer(GLuint index, GLint size, GLenum type, GLboolean normalized, GLsizei stride, const void *pointer) {
    webgl2_glVertexAttribPointer(index, size, type, normalized, stride, pointer);
}

void impl_glUniformMatrix2x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix2x3fv(location, count, transpose, value);
}

void impl_glUniformMatrix3x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix3x2fv(location, count, transpose, value);
}

void impl_glUniformMatrix2x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix2x4fv(location, count, transpose, value);
}

void impl_glUniformMatrix4x2fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix4x2fv(location, count, transpose, value);
}

void impl_glUniformMatrix3x4fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix3x4fv(location, count, transpose, value);
}

void impl_glUniformMatrix4x3fv(GLint location, GLsizei count, GLboolean transpose, const GLfloat *value) {
    webgl2_glUniformMatrix4x3fv(location, count, transpose, value);
}

void impl_glBindBufferRange(GLenum target, GLuint index, GLuint buffer, GLintptr offset, GLsizeiptr size) {
    webgl2_glBindBufferRange(target, index, buffer, offset, size);
}

void impl_glVertexAttribIPointer(GLuint index, GLint size, GLenum type, GLsizei stride, const void *pointer) {
    webgl2_glVertexAttribIPointer(index, size, type, stride, pointer);
}

void impl_glUniform1uiv(GLint location, GLsizei count, const GLuint *value) {
    webgl2_glUniform1uiv(location, count, value);
}

void impl_glUniform2uiv(GLint location, GLsizei count, const GLuint *value) {
    webgl2_glUniform2uiv(location, count, value);
}

void impl_glUniform3uiv(GLint location, GLsizei count, const GLuint *value) {
    webgl2_glUniform3uiv(location, count, value);
}

void impl_glUniform4uiv(GLint location, GLsizei count, const GLuint *value) {
    webgl2_glUniform4uiv(location, count, value);
}

void impl_glClearBufferiv(GLenum buffer, GLint drawbuffer, const GLint *value) {
    webgl2_glClearBufferiv(buffer, drawbuffer, value);
}

void impl_glClearBufferuiv(GLenum buffer, GLint drawbuffer, const GLuint *value) {
    webgl2_glClearBufferuiv(buffer, drawbuffer, value);
}

void impl_glClearBufferfv(GLenum buffer, GLint drawbuffer, const GLfloat *value) {
    webgl2_glClearBufferfv(buffer, drawbuffer, value);
}

void impl_glClearBufferfi(GLenum buffer, GLint drawbuffer, GLfloat depth, GLint stencil) {
    webgl2_glClearBufferfi(buffer, drawbuffer, depth, stencil);
}

void impl_glBindRenderbuffer(GLenum target, GLuint renderbuffer) {
    webgl2_glBindRenderbuffer(target, renderbuffer);
}

void impl_glDeleteRenderbuffers(GLsizei n, const GLuint *renderbuffers) {
    webgl2_glDeleteRenderbuffers(n, renderbuffers);
}

void impl_glGenRenderbuffers(GLsizei n, GLuint *renderbuffers) {
    webgl2_glGenRenderbuffers(n, renderbuffers);
}

void impl_glBindFramebuffer(GLenum target, GLuint framebuffer) {
    webgl2_glBindFramebuffer(target, framebuffer);
}

void impl_glDeleteFramebuffers(GLsizei n, const GLuint *framebuffers) {
    webgl2_glDeleteFramebuffers(n, framebuffers);
}

void impl_glGenFramebuffers(GLsizei n, GLuint *framebuffers) {
    webgl2_glGenFramebuffers(n, framebuffers);
}

void impl_glFramebufferTexture2D(GLenum target, GLenum attachment, GLenum textarget, GLuint texture, GLint level) {
    webgl2_glFramebufferTexture2D(target, attachment, textarget, texture, level);
}

void impl_glFramebufferRenderbuffer(GLenum target, GLenum attachment, GLenum renderbuffertarget, GLuint renderbuffer) {
    webgl2_glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer);
}

void impl_glGenerateMipmap(GLenum target) {
    webgl2_glGenerateMipmap(target);
}

void impl_glBlitFramebuffer(GLint srcX0, GLint srcY0, GLint srcX1, GLint srcY1, GLint dstX0, GLint dstY0, GLint dstX1, GLint dstY1, GLbitfield mask, GLenum filter) {
    webgl2_glBlitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter);
}

void impl_glRenderbufferStorageMultisample(GLenum target, GLsizei samples, GLenum internalformat, GLsizei width, GLsizei height) {
    webgl2_glRenderbufferStorageMultisample(target, samples, internalformat, width, height);
}

void impl_glFramebufferTextureLayer(GLenum target, GLenum attachment, GLuint texture, GLint level, GLint layer) {
    webgl2_glFramebufferTextureLayer(target, attachment, texture, level, layer);
}

void *impl_glMapBufferRange(GLenum target, GLintptr offset, GLsizeiptr length, GLbitfield access) {
    return webgl2_glMapBufferRange(target, offset, length, access);
}

void impl_glBindVertexArray(GLuint array) {
    webgl2_glBindVertexArray(array);
}

void impl_glDeleteVertexArrays(GLsizei n, const GLuint *arrays) {
    webgl2_glDeleteVertexArrays(n, arrays);
}

void impl_glGenVertexArrays(GLsizei n, GLuint *arrays) {
    webgl2_glGenVertexArrays(n, arrays);
}

void impl_glDrawArraysInstanced(GLenum mode, GLint first, GLsizei count, GLsizei instancecount) {
    webgl2_glDrawArraysInstanced(mode, first, count, instancecount);
}

void impl_glDrawElementsInstanced(GLenum mode, GLsizei count, GLenum type, const void *indices, GLsizei instancecount) {
    webgl2_glDrawElementsInstanced(mode, count, type, indices, instancecount);
}

GLuint impl_glGetUniformBlockIndex(GLuint program, const GLchar *uniformBlockName) {
    return webgl2_glGetUniformBlockIndex(program, uniformBlockName);
}

void impl_glGetActiveUniformBlockiv(GLuint program, GLuint uniformBlockIndex, GLenum pname, GLint *params) {
    webgl2_glGetActiveUniformBlockiv(program, uniformBlockIndex, pname, params);
}

void impl_glGetActiveUniformBlockName(GLuint program, GLuint uniformBlockIndex, GLsizei bufSize, GLsizei *length, GLchar *uniformBlockName) {
    webgl2_glGetActiveUniformBlockName(program, uniformBlockIndex, bufSize, length, uniformBlockName);
}

void impl_glUniformBlockBinding(GLuint program, GLuint uniformBlockIndex, GLuint uniformBlockBinding) {
    webgl2_glUniformBlockBinding(program, uniformBlockIndex, uniformBlockBinding);
}

GLsync impl_glFenceSync(GLenum condition, GLbitfield flags) {
    return webgl2_glFenceSync(condition, flags);
}

void impl_glDeleteSync(GLsync sync) {
    webgl2_glDeleteSync(sync);
}

GLenum impl_glClientWaitSync(GLsync sync, GLbitfield flags, GLuint64 timeout) {
    return webgl2_glClientWaitSync(sync, flags, timeout);
}

void impl_glGenSamplers(GLsizei count, GLuint *samplers) {
    webgl2_glGenSamplers(count, samplers);
}

void impl_glDeleteSamplers(GLsizei count, const GLuint *samplers) {
    webgl2_glDeleteSamplers(count, samplers);
}

void impl_glBindSampler(GLuint unit, GLuint sampler) {
    webgl2_glBindSampler(unit, sampler);
}

void impl_glSamplerParameteri(GLuint sampler, GLenum pname, GLint param) {
    webgl2_glSamplerParameteri(sampler, pname, param);
}

void impl_glSamplerParameterf(GLuint sampler, GLenum pname, GLfloat param) {
    webgl2_glSamplerParameterf(sampler, pname, param);
}

void impl_glVertexAttribDivisor(GLuint index, GLuint divisor) {
    webgl2_glVertexAttribDivisor(index, divisor);
}

PyObject * lookup;

static void fn(const char * name, void * ptr) {
    PyDict_SetItemString(lookup, name, PyLong_FromVoidPtr(ptr));
}

static PyObject * load_opengl_function(PyObject * self, PyObject * arg) {
    PyObject * res = PyDict_GetItem(lookup, arg);
    if (!res) {
        return NULL;
    }
    Py_INCREF(res);
    return res;
}

static PyMethodDef module_methods[] = {
    {"load_opengl_function", (PyCFunction)load_opengl_function, METH_O, NULL},
    {0},
};

static PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "webgl2", NULL, -1, module_methods};

extern PyObject * PyInit_webgl2() {
    PyObject * module = PyModule_Create(&module_def);

    lookup = PyDict_New();
    fn("glCullFace", impl_glCullFace);
    fn("glClear", impl_glClear);
    fn("glTexParameteri", impl_glTexParameteri);
    fn("glTexImage2D", impl_glTexImage2D);
    fn("glDepthMask", impl_glDepthMask);
    fn("glDisable", impl_glDisable);
    fn("glEnable", impl_glEnable);
    fn("glFlush", impl_glFlush);
    fn("glDepthFunc", impl_glDepthFunc);
    fn("glReadBuffer", impl_glReadBuffer);
    fn("glReadPixels", impl_glReadPixels);
    fn("glGetError", impl_glGetError);
    fn("glGetIntegerv", impl_glGetIntegerv);
    fn("glGetString", impl_glGetString);
    fn("glViewport", impl_glViewport);
    fn("glTexSubImage2D", impl_glTexSubImage2D);
    fn("glBindTexture", impl_glBindTexture);
    fn("glDeleteTextures", impl_glDeleteTextures);
    fn("glGenTextures", impl_glGenTextures);
    fn("glTexImage3D", impl_glTexImage3D);
    fn("glTexSubImage3D", impl_glTexSubImage3D);
    fn("glActiveTexture", impl_glActiveTexture);
    fn("glBlendFuncSeparate", impl_glBlendFuncSeparate);
    fn("glGenQueries", impl_glGenQueries);
    fn("glBeginQuery", impl_glBeginQuery);
    fn("glEndQuery", impl_glEndQuery);
    fn("glGetQueryObjectuiv", impl_glGetQueryObjectuiv);
    fn("glBindBuffer", impl_glBindBuffer);
    fn("glDeleteBuffers", impl_glDeleteBuffers);
    fn("glGenBuffers", impl_glGenBuffers);
    fn("glBufferData", impl_glBufferData);
    fn("glBufferSubData", impl_glBufferSubData);
    fn("glUnmapBuffer", impl_glUnmapBuffer);
    fn("glBlendEquationSeparate", impl_glBlendEquationSeparate);
    fn("glDrawBuffers", impl_glDrawBuffers);
    fn("glStencilOpSeparate", impl_glStencilOpSeparate);
    fn("glStencilFuncSeparate", impl_glStencilFuncSeparate);
    fn("glStencilMaskSeparate", impl_glStencilMaskSeparate);
    fn("glAttachShader", impl_glAttachShader);
    fn("glCompileShader", impl_glCompileShader);
    fn("glCreateProgram", impl_glCreateProgram);
    fn("glCreateShader", impl_glCreateShader);
    fn("glDeleteProgram", impl_glDeleteProgram);
    fn("glDeleteShader", impl_glDeleteShader);
    fn("glEnableVertexAttribArray", impl_glEnableVertexAttribArray);
    fn("glGetActiveAttrib", impl_glGetActiveAttrib);
    fn("glGetActiveUniform", impl_glGetActiveUniform);
    fn("glGetAttribLocation", impl_glGetAttribLocation);
    fn("glGetProgramiv", impl_glGetProgramiv);
    fn("glGetProgramInfoLog", impl_glGetProgramInfoLog);
    fn("glGetShaderiv", impl_glGetShaderiv);
    fn("glGetShaderInfoLog", impl_glGetShaderInfoLog);
    fn("glGetUniformLocation", impl_glGetUniformLocation);
    fn("glLinkProgram", impl_glLinkProgram);
    fn("glShaderSource", impl_glShaderSource);
    fn("glUseProgram", impl_glUseProgram);
    fn("glUniform1i", impl_glUniform1i);
    fn("glUniform1fv", impl_glUniform1fv);
    fn("glUniform2fv", impl_glUniform2fv);
    fn("glUniform3fv", impl_glUniform3fv);
    fn("glUniform4fv", impl_glUniform4fv);
    fn("glUniform1iv", impl_glUniform1iv);
    fn("glUniform2iv", impl_glUniform2iv);
    fn("glUniform3iv", impl_glUniform3iv);
    fn("glUniform4iv", impl_glUniform4iv);
    fn("glUniformMatrix2fv", impl_glUniformMatrix2fv);
    fn("glUniformMatrix3fv", impl_glUniformMatrix3fv);
    fn("glUniformMatrix4fv", impl_glUniformMatrix4fv);
    fn("glVertexAttribPointer", impl_glVertexAttribPointer);
    fn("glUniformMatrix2x3fv", impl_glUniformMatrix2x3fv);
    fn("glUniformMatrix3x2fv", impl_glUniformMatrix3x2fv);
    fn("glUniformMatrix2x4fv", impl_glUniformMatrix2x4fv);
    fn("glUniformMatrix4x2fv", impl_glUniformMatrix4x2fv);
    fn("glUniformMatrix3x4fv", impl_glUniformMatrix3x4fv);
    fn("glUniformMatrix4x3fv", impl_glUniformMatrix4x3fv);
    fn("glBindBufferRange", impl_glBindBufferRange);
    fn("glVertexAttribIPointer", impl_glVertexAttribIPointer);
    fn("glUniform1uiv", impl_glUniform1uiv);
    fn("glUniform2uiv", impl_glUniform2uiv);
    fn("glUniform3uiv", impl_glUniform3uiv);
    fn("glUniform4uiv", impl_glUniform4uiv);
    fn("glClearBufferiv", impl_glClearBufferiv);
    fn("glClearBufferuiv", impl_glClearBufferuiv);
    fn("glClearBufferfv", impl_glClearBufferfv);
    fn("glClearBufferfi", impl_glClearBufferfi);
    fn("glBindRenderbuffer", impl_glBindRenderbuffer);
    fn("glDeleteRenderbuffers", impl_glDeleteRenderbuffers);
    fn("glGenRenderbuffers", impl_glGenRenderbuffers);
    fn("glBindFramebuffer", impl_glBindFramebuffer);
    fn("glDeleteFramebuffers", impl_glDeleteFramebuffers);
    fn("glGenFramebuffers", impl_glGenFramebuffers);
    fn("glFramebufferTexture2D", impl_glFramebufferTexture2D);
    fn("glFramebufferRenderbuffer", impl_glFramebufferRenderbuffer);
    fn("glGenerateMipmap", impl_glGenerateMipmap);
    fn("glBlitFramebuffer", impl_glBlitFramebuffer);
    fn("glRenderbufferStorageMultisample", impl_glRenderbufferStorageMultisample);
    fn("glFramebufferTextureLayer", impl_glFramebufferTextureLayer);
    fn("glMapBufferRange", impl_glMapBufferRange);
    fn("glBindVertexArray", impl_glBindVertexArray);
    fn("glDeleteVertexArrays", impl_glDeleteVertexArrays);
    fn("glGenVertexArrays", impl_glGenVertexArrays);
    fn("glDrawArraysInstanced", impl_glDrawArraysInstanced);
    fn("glDrawElementsInstanced", impl_glDrawElementsInstanced);
    fn("glGetUniformBlockIndex", impl_glGetUniformBlockIndex);
    fn("glGetActiveUniformBlockiv", impl_glGetActiveUniformBlockiv);
    fn("glGetActiveUniformBlockName", impl_glGetActiveUniformBlockName);
    fn("glUniformBlockBinding", impl_glUniformBlockBinding);
    fn("glFenceSync", impl_glFenceSync);
    fn("glDeleteSync", impl_glDeleteSync);
    fn("glClientWaitSync", impl_glClientWaitSync);
    fn("glGenSamplers", impl_glGenSamplers);
    fn("glDeleteSamplers", impl_glDeleteSamplers);
    fn("glBindSampler", impl_glBindSampler);
    fn("glSamplerParameteri", impl_glSamplerParameteri);
    fn("glSamplerParameterf", impl_glSamplerParameterf);
    fn("glVertexAttribDivisor", impl_glVertexAttribDivisor);
    return module;
}
