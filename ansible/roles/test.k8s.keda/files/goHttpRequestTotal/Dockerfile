FROM golang:1.19 as builder

WORKDIR /workspace
COPY go.mod go.mod
COPY go.sum go.sum
COPY main.go main.go
RUN go mod download

RUN CGO_ENABLED=0 GOOS=${TARGETOS:-linux} GOARCH=${TARGETARCH} go build -a -o manager main.go

FROM gcr.io/distroless/static:nonroot
WORKDIR /
COPY --from=builder /workspace/manager .
USER 65532:65532

ENTRYPOINT [ "/manager" ]