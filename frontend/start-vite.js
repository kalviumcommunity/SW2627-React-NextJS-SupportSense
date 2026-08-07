import { createServer } from 'vite';

async function start() {
  try {
    const server = await createServer({
      configFile: './vite.config.ts',
      server: {
        port: 5173,
        host: true
      }
    });
    await server.listen();
    server.printUrls();
    console.log('Vite server started programmatically!');
  } catch (err) {
    console.error('Error starting Vite:', err);
  }
}

start();
