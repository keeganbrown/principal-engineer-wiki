---
title: Load Balancers and Content Delivery Networks (CDNs)
category: technology
summary: Load balancers spread traffic across healthy servers, and content delivery networks serve content from locations close to users — together they're the front door that makes a service fast, scalable, and resilient.
tags: [networking, scalability, availability, performance]
---

# Load Balancers and Content Delivery Networks (CDNs)

> **In one sentence:** Load balancers spread traffic across healthy servers, and content delivery networks serve content from locations close to users — together they're the front door that makes a service fast, scalable, and resilient.

## The idea

A **load balancer** receives incoming requests and forwards each one to one of several servers behind it. It checks which servers are healthy and stops sending traffic to broken ones. To users, the service has one address; behind it, servers come and go.

Load balancers work at two layers of the standard networking model (the OSI model, whose seven layers run from cables up to applications):

- **Layer 4** — the transport layer. It forwards network connections without reading them. Fast and simple.
- **Layer 7** — the application layer. It reads HTTP requests, so it can route by path or header (`/api` to one service, `/images` to another), terminate TLS (Transport Layer Security, the encryption behind HTTPS), so servers behind it receive plain requests, and add retries or rate limits. Long-lived connections, such as gRPC or WebSockets, pin traffic to one server at Layer 4, so new servers get no load; spreading individual requests needs Layer 7. A **reverse proxy** such as NGINX or Envoy does this job too.

A **content delivery network (CDN)** is a worldwide network of servers that keep cached copies of your content near users. A visitor in Sydney gets your images from Sydney, not from Virginia. Modern CDNs also absorb attacks, terminate TLS, and run small bits of code at the edge.

## Why it matters

- **Scaling out needs a front door.** Adding servers (horizontal scaling) only helps if traffic is spread across them.
- **Users don't see single-server failures.** Health checks route around a crashed server or a bad deploy without users noticing.
- **Distance is latency.** A round trip from Sydney to Virginia takes over 150 milliseconds in practice, and the speed of light in fiber sets a floor you can't engineer away; serving from nearby cuts that out for every cached asset.
- **Protection comes built in.** CDNs and cloud load balancers absorb floods of traffic that would overwhelm your servers.

The cost: another layer to configure and debug, cache rules that can serve stale or wrong content, and — for a CDN — a third party in your request path.

## How to apply it

- **Make health checks meaningful.** A check that returns "OK" while the database is unreachable keeps sending traffic to a broken server. Check what the server needs to do its job, but tolerate brief blips: when every server shares one database, a check that fails on its slightest delay pulls every server out at once. Alert on shared dependencies separately.
- **Drain connections on deploy.** Stop sending new requests to a server, let current ones finish, then shut it down. This is what makes zero-downtime deploys possible ([[continuous-delivery]]), whether rolling (servers replaced a few at a time) or blue-green (a full new set of servers, with traffic switched over at once).
- **Avoid sticky sessions where you can.** Pinning a user to one server makes scaling and failover harder. Keep session state in a shared store instead.
- **Put static assets on a CDN with long cache lifetimes.** Change the file name when the content changes (`app.3f9a2c.js`) so you never need to purge.
- **Be careful caching dynamic pages.** Cache keys must include anything that changes the response, such as language or login state ([[caching]]).
- **Set timeouts at the edge.** The load balancer's request timeout should be longer than your server's, so the server times out first and returns a real error, rather than the load balancer cutting the connection mid-response ([[retries-and-timeouts]]). Idle keep-alive timeouts follow the opposite rule: the server's must be longer than the load balancer's, or you get intermittent 502 errors.

## Example

A news site serves everything from four servers in one region. When a story goes viral, traffic grows tenfold in minutes, servers saturate, and readers abroad wait seconds for each page.

They put a CDN in front: images, scripts, and styles are cached for a year with hashed file names, and article pages are cached for 60 seconds. A Layer 7 load balancer behind the CDN routes `/api` to an autoscaling group and checks each server's health every 10 seconds.

During the next viral story, the CDN serves 95% of requests and the servers barely notice. The trade-off appears in the newsroom: a correction takes up to a minute to show up worldwide. The team adds an instant purge for article pages, wired into the publishing tool, and accepts the 60-second window for everything else.

Purges take seconds to spread and are rate-limited. Purging many hot pages at once also sends a burst to the origin (the servers the CDN fetches from), so mass corrections still wait out the window.

## Common traps

- **Health checks that are too shallow or too deep.** Too shallow misses broken servers; too deep makes every server fail together when one dependency hiccups.
- **Caching personalized pages publicly.** One user's account page served to another is a data breach.
- **The load balancer as a single point of failure.** Use the provider's managed, redundant load balancers, or run at least two. The same goes for the CDN: know how you'd bypass it, and who decides, if it goes down.
- **Retries at every layer.** Load balancer, client library, and application each making three attempts turns one failure into 27 calls on the backend ([[retries-and-timeouts]]).
- **Forgetting real client IPs.** Behind a proxy, every request comes from the proxy's address unless you read the forwarded header — and only trust that header from your own proxies.

## When it doesn't apply

A single internal tool with a handful of users doesn't need a CDN, and may not need a load balancer if one server and a quick restart are acceptable. Container platforms and cloud services often include load balancing, so you configure it rather than run it yourself ([[containers-and-kubernetes]]).

## Related

- [[caching]] — CDNs are caches; the same staleness rules apply.
- [[containers-and-kubernetes]] — platforms that load-balance across containers for you.
- [[retries-and-timeouts]] — set timeouts consistently across layers.
- [[circuit-breaker]] — the client-side partner to health checks: stop calling a backend the balancer can't route around.
- [[object-storage]] — a common origin for CDN-served files.
