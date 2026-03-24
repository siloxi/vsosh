FROM node:18-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

RUN npm ci --prefer-offline --no-audit --progress=false

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

RUN addgroup -S nextjs && adduser -S nextjs -G nextjs

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

RUN npm ci --production --prefer-offline --no-audit --progress=false

RUN chown -R nextjs:nextjs /app
USER nextjs

ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "run", "start"]
