import React from "react"
import Layout from "@theme/Layout"
import useDocusaurusContext from "@docusaurus/useDocusaurusContext"
import styles from "./index.module.css"
import Card from "../components/Card"

function Home() {
  const context = useDocusaurusContext();

  return (
    <Layout title="Homepage" description="Evmos Docs">
      <main>
        <br />
        <h1 align="center" style={{ fontWeight: '750' }}>Welcome to Evmos Docs</h1>
        <section className={styles.features}>
          <div className="container">
            <div className="row cards__container">
              <Card
                to="./develop/build-a-dApp/run-a-node"
                header={{
                  label: "🚀 Launch Your Local Node",
                }}
                body={{
                  label:
                    "Getting started on Evmos is simple and easy with local node",
                }}
              />

              <Card
                to="./use"
                header={{
                  label: "☄️ Learn about Evmos",
                }}
                body={{
                  label:
                    "Discover why Evmos is the flagship EVM on the Cosmos Ecosystem",
                }}
              />

              <Card
                to="./validate"
                header={{
                  label: "😎 Become a Validator",
                }}
                body={{
                  label:
                    "Join Evmos's Proof-of-Stake protocol to help secure the network and earn rewards",
                }}
              />

              <Card
                to="./api"
                header={{
                  label: "💻 View Evmos APIs",
                }}
                body={{
                  label:
                    "Access low-level protocol interfaces to build your custom dapp",
                }}
              />

              <Card
                to="./develop/build-a-dApp/run-a-node/evmosd"
                header={{
                  label: "🛠️ Launch dApp on Evmos",
                }}
                body={{
                  label:
                    "Learn everything you need to deploy an EVM-compatible smart contract",
                }}
              />

              <Card
                to="https://github.com/evmos"
                header={{
                  label: "🛠️ Contribute to Evmos",
                }}
                body={{
                  label:
                    "Contribute to the thriving ecosystem of Evmos and its open-source initiatives",
                }}
              />
            </div>
          </div>
        </section>
      </main>
    </Layout>
  )
}

export default Home