package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/iotaledger/hive.go/lo"
	"github.com/iotaledger/hive.go/serializer/v2/serix"
	iotago "github.com/iotaledger/iota.go/v4"
	apipkg "github.com/iotaledger/iota.go/v4/api"
	"github.com/iotaledger/iota.go/v4/hexutil"
	"github.com/iotaledger/iota.go/v4/tpkg"
	"github.com/iotaledger/tip-tools/test-vectors/examples"
	"github.com/itchyny/json2yaml"
)

const (
	// TestTokenSupply is a test token supply constant.
	TestTokenSupply        = 2_779_530_283_277_761
	ProtocolParameters     = "Protocol Parameters"
	CommitmentID           = "Commitment ID"
	TransactionID          = "Transaction ID"
	BasicBlockIDTx         = "Basic Block ID Transaction"
	BasicBlockIDTaggedData = "Basic Block ID Tagged Data"
	BasicBlockIDNoPayload  = "Basic Block ID No Payload"
	ValidationBlockID      = "Validation Block ID"
	MultiAddress           = "Multi Address"
	OutputIdProof          = "Output ID Proof"
	RestrictedAddress      = "Restricted Address"
	InfoResponse           = "Info Response"
	StorageScoreDelegation = "Storage Score Delegation"
	StorageScoreBasic      = "Storage Score Basic"
	StorageScoreAccount    = "Storage Score Account"
	StorageScoreNFT        = "Storage Score NFT"
	StorageScoreFoundry    = "Storage Score Foundry"
	StorageScoreAnchor     = "Storage Score Anchor"
)

var (
	genesisTimestamp = time.Unix(1695275822, 0) // 2023-09-21 13:57:02 +0800 CST
	api              = iotago.V3API(
		iotago.NewV3SnapshotProtocolParameters(
			// Fix the genesis timestamp so we have a consistent protocol parameters hash for the test vectors.
			iotago.WithTimeProviderOptions(0, genesisTimestamp.Unix(), 10, 13),
			// Set non-zero values so we can produce meaningful work score test vectors.
			iotago.WithWorkScoreOptions(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
		),
	)
	supportedObjects = []string{
		ProtocolParameters,
		CommitmentID,
		TransactionID,
		BasicBlockIDTx,
		BasicBlockIDTaggedData,
		BasicBlockIDNoPayload,
		ValidationBlockID,
		MultiAddress,
		OutputIdProof,
		RestrictedAddress,
		InfoResponse,
		StorageScoreDelegation,
		StorageScoreBasic,
		StorageScoreAccount,
		StorageScoreNFT,
		StorageScoreFoundry,
		StorageScoreAnchor,
	}

	isYaml = false
)

func main() {
	if len(os.Args) <= 1 {
		return
	}
	name := os.Args[1]

	if len(os.Args) >= 3 {
		isYaml, _ = strconv.ParseBool(os.Args[2])
	}

	switch name {
	case ProtocolParameters:
		protocolParameters()
	case CommitmentID:
		commitmentExample()
	case TransactionID:
		transactionIDExample()
	case BasicBlockIDTx:
		basicBlockIDTransactionExample()
	case BasicBlockIDTaggedData:
		basicBlockIDTaggedDataExample()
	case BasicBlockIDNoPayload:
		basicBlockIDNoPayloadExample()
	case ValidationBlockID:
		validationBlockIDExample()
	case MultiAddress:
		multiAddressTestVector()
	case OutputIdProof:
		outputIdProof()
	case RestrictedAddress:
		restrictedAddresses()
	case InfoResponse:
		infoResponse()
	case StorageScoreDelegation:
		storageScoreDelegation()
	case StorageScoreBasic:
		storageScoreBasic()
	case StorageScoreAccount:
		storageScoreAccount()
	case StorageScoreNFT:
		storageScoreNFT()
	case StorageScoreFoundry:
		storageScoreFoundry()
	case StorageScoreAnchor:
		storageScoreAnchor()
	default:
		fmt.Println("Usage: go run main.go \"[object name]\" [isYaml]")
		fmt.Println("Supported object:")
		for _, o := range supportedObjects {
			fmt.Println("\t -", o)
		}
	}
}

func protocolParameters() {
	printIdentifierAndWorkScoreTestVector("Protocol Parameters", api.ProtocolParameters(), lo.Return1(api.ProtocolParameters().Hash()).ToHex(), false)
}

func commitmentExample() {
	previousCommitmentID := iotago.MustCommitmentIDFromHexString("0x5f400a6621684e7b260f353b3937113c153c387c5c2f7110463a2f1b2f1c392a581e192d")
	rootsID := iotago.MustIdentifierFromHexString("0x533543553e75065c0c115c220624400b02693c6177284b4f1b7748610c515968")

	commitment := iotago.Commitment{
		ProtocolVersion:      api.Version(),
		Slot:                 18,
		PreviousCommitmentID: previousCommitmentID,
		RootsID:              rootsID,
		CumulativeWeight:     89,
		ReferenceManaCost:    144,
	}

	printIdentifierAndWorkScoreTestVector("Slot Commitment", commitment, commitment.MustID().ToHex(), false)
}

func transactionIDExample() {
	tx := examples.SignedTransaction(api)
	printIdentifierAndWorkScoreTestVector("Transaction", tx, lo.PanicOnErr(tx.ID()).ToHex(), false)
}

func basicBlockIDNoPayloadExample() {
	block := examples.BasicBlockWithoutPayload(api)

	printIdentifierAndWorkScoreTestVector("Block", block, block.MustID().ToHex(), true)
}

func basicBlockIDTransactionExample() {
	block := examples.BasicBlockWithPayload(api, examples.SignedTransaction(api))

	printIdentifierAndWorkScoreTestVector("Block", block, block.MustID().ToHex(), true)
}

func basicBlockIDTaggedDataExample() {
	taggedData := iotago.TaggedData{
		Tag:  lo.PanicOnErr(hexutil.DecodeHex("0x746167")),
		Data: lo.PanicOnErr(hexutil.DecodeHex("0x6c754128356c071e5549764a48427b")),
	}
	block := examples.BasicBlockWithPayload(api, &taggedData)
	printIdentifierAndWorkScoreTestVector("Block", block, block.MustID().ToHex(), true)
}

func validationBlockIDExample() {
	block := examples.ValidationBlock(api)
	printIdentifierAndWorkScoreTestVector("Block", block, block.MustID().ToHex(), false)
}

// Used in TIP-52.
func multiAddressTestVector() {
	addr := &iotago.MultiAddress{
		Addresses: []*iotago.AddressWithWeight{
			{
				Address: &iotago.Ed25519Address{0x52, 0xfd, 0xfc, 0x07, 0x21, 0x82, 0x65, 0x4f, 0x16, 0x3f, 0x5f, 0x0f, 0x9a, 0x62, 0x1d, 0x72, 0x95, 0x66, 0xc7, 0x4d, 0x10, 0x03, 0x7c, 0x4d, 0x7b, 0xbb, 0x04, 0x07, 0xd1, 0xe2, 0xc6, 0x49},
				Weight:  1,
			},
			{
				Address: &iotago.Ed25519Address{0x53, 0xfd, 0xfc, 0x07, 0x21, 0x82, 0x65, 0x4f, 0x16, 0x3f, 0x5f, 0x0f, 0x9a, 0x62, 0x1d, 0x72, 0x95, 0x66, 0xc7, 0x4d, 0x10, 0x03, 0x7c, 0x4d, 0x7b, 0xbb, 0x04, 0x07, 0xd1, 0xe2, 0xc6, 0x49},
				Weight:  1,
			},
			{
				Address: &iotago.Ed25519Address{0x54, 0xfd, 0xfc, 0x07, 0x21, 0x82, 0x65, 0x4f, 0x16, 0x3f, 0x5f, 0x0f, 0x9a, 0x62, 0x1d, 0x72, 0x95, 0x66, 0xc7, 0x4d, 0x10, 0x03, 0x7c, 0x4d, 0x7b, 0xbb, 0x04, 0x07, 0xd1, 0xe2, 0xc6, 0x49},
				Weight:  1,
			},
			{
				Address: &iotago.AccountAddress{0x55, 0xfd, 0xfc, 0x07, 0x21, 0x82, 0x65, 0x4f, 0x16, 0x3f, 0x5f, 0x0f, 0x9a, 0x62, 0x1d, 0x72, 0x95, 0x66, 0xc7, 0x4d, 0x10, 0x03, 0x7c, 0x4d, 0x7b, 0xbb, 0x04, 0x07, 0xd1, 0xe2, 0xc6, 0x49},
				Weight:  2,
			},
			{
				Address: &iotago.NFTAddress{0x56, 0xfd, 0xfc, 0x07, 0x21, 0x82, 0x65, 0x4f, 0x16, 0x3f, 0x5f, 0x0f, 0x9a, 0x62, 0x1d, 0x72, 0x95, 0x66, 0xc7, 0x4d, 0x10, 0x03, 0x7c, 0x4d, 0x7b, 0xbb, 0x04, 0x07, 0xd1, 0xe2, 0xc6, 0x49},
				Weight:  3,
			},
		},
		Threshold: 2,
	}

	addrRef := iotago.NewMultiAddressReferenceFromMultiAddress(addr)

	fmt.Printf("%s\n\n", jsonify(addr))

	fmt.Printf("%s\n\n", addrRef.Bech32(iotago.PrefixMainnet))
}

func outputIdProof() {
	type outputIDProofExample struct {
		tx *iotago.SignedTransaction
	}

	singleOutput := outputIDProofExample{
		tx: examples.SignedTransactionOutputIdProof(api, 1),
	}

	fiveOutputs := outputIDProofExample{
		tx: examples.SignedTransactionOutputIdProof(api, 5),
	}

	manyOutputs := outputIDProofExample{
		tx: examples.SignedTransactionOutputIdProof(api, 32),
	}

	fmt.Println("============================ SINGLE OUTPUT ==============================")

	singleOutputProof := lo.PanicOnErr(iotago.OutputIDProofFromTransaction(singleOutput.tx.Transaction, 0))
	printBinary("Signed Transaction (1 Output)", singleOutput.tx)
	printJson("Output ID Proof (Output Index 0)", singleOutputProof)
	printBinary("Output ID Proof (Output Index 0)", singleOutputProof)
	if isYaml {
		printYaml("Output ID Proof (Output Index 0)", singleOutputProof)
	}

	fmt.Println("============================ 5 OUTPUTS ==============================")

	fiveOutputsProof := lo.PanicOnErr(iotago.OutputIDProofFromTransaction(fiveOutputs.tx.Transaction, 2))
	printBinary("Signed Transaction (5 Outputs)", fiveOutputs.tx)
	printJson("Output ID Proof (Output Index 2)", fiveOutputsProof)
	printBinary("Output ID Proof (Output Index 2)", fiveOutputsProof)
	if isYaml {
		printYaml("Output ID Proof (Output Index 2)", fiveOutputsProof)
	}

	fmt.Println("============================ 32 OUTPUTS ==============================")

	manyOutputsProof0 := lo.PanicOnErr(iotago.OutputIDProofFromTransaction(manyOutputs.tx.Transaction, 0))
	printBinary("Signed Transaction (32 Outputs)", manyOutputs.tx)
	printJson("Output ID Proof (Output Index 0)", manyOutputsProof0)
	printBinary("Output ID Proof (Output Index 0)", manyOutputsProof0)
	if isYaml {
		printYaml("Output ID Proof (Output Index 0)", manyOutputsProof0)
	}

	manyOutputsProof28 := lo.PanicOnErr(iotago.OutputIDProofFromTransaction(manyOutputs.tx.Transaction, 28))
	printJson("Output ID Proof (Output Index 28)", manyOutputsProof28)
	printBinary("Output ID Proof (Output Index 28)", manyOutputsProof28)
}

func restrictedAddresses() {
	ed25519PubKey := lo.PanicOnErr(hexutil.DecodeHex("0x6f1581709bb7b1ef030d210db18e3b0ba1c776fba65d8cdaad05415142d189f8"))

	type NamedAddress struct {
		name    string
		address iotago.Address
	}

	namedAddresses := []NamedAddress{
		{
			name:    "Ed25519 Address",
			address: iotago.Ed25519AddressFromPubKey(ed25519PubKey),
		},
		{
			name:    "Account Address",
			address: tpkg.RandAccountAddress(),
		},
		{
			name:    "NFT Address",
			address: tpkg.RandNFTAddress(),
		},
	}

	capabilities := []iotago.AddressCapabilitiesBitMask{
		iotago.AddressCapabilitiesBitMaskWithCapabilities(),
		iotago.AddressCapabilitiesBitMaskWithCapabilities(iotago.WithAddressCanReceiveAnything()),
		iotago.AddressCapabilitiesBitMaskWithCapabilities(iotago.WithAddressCanReceiveNativeTokens(true)),
	}

	for _, namedAddress := range namedAddresses {
		printAddress(namedAddress.name, "Plain", namedAddress.address)

		for i, capability := range capabilities {
			info := ""
			switch i {
			case 0:
				info = "Every Capability Disallowed"
			case 1:
				info = "Every Capability Allowed"
			case 2:
				info = "Can receive Native Tokens"
			}

			restrictedAddress := iotago.RestrictedAddress{
				Address:             namedAddress.address,
				AllowedCapabilities: capability,
			}

			printAddress(fmt.Sprintf("Restricted %s", namedAddress.name), info, &restrictedAddress)
		}
	}
}

// core API responses
func infoResponse() {
	response := &apipkg.InfoResponse{
		Name:    "test",
		Version: "2.0.0",
		Status: &apipkg.InfoResNodeStatus{
			IsHealthy:                   false,
			AcceptedTangleTime:          time.Unix(1690879505, 0).UTC(),
			RelativeAcceptedTangleTime:  time.Unix(1690879505, 0).UTC(),
			ConfirmedTangleTime:         time.Unix(1690879505, 0).UTC(),
			RelativeConfirmedTangleTime: time.Unix(1690879505, 0).UTC(),
			LatestCommitmentID:          tpkg.RandCommitmentID(),
			LatestFinalizedSlot:         1,
			LatestAcceptedBlockSlot:     2,
			LatestConfirmedBlockSlot:    3,
			PruningEpoch:                4,
		},
		Metrics: &apipkg.InfoResNodeMetrics{
			BlocksPerSecond:          1.1,
			ConfirmedBlocksPerSecond: 2.2,
			ConfirmationRate:         3.3,
		},
		ProtocolParameters: []*apipkg.InfoResProtocolParameters{
			{
				StartEpoch: 0,
				Parameters: api.ProtocolParameters(),
			},
		},
		BaseToken: &apipkg.InfoResBaseToken{
			Name:         "Shimmer",
			TickerSymbol: "SMR",
			Unit:         "SMR",
			Subunit:      "glow",
			Decimals:     6,
		},
		Features: []string{"test"},
	}

	printYaml("Info Response", response)
}

func storageScoreDelegation() {
	delegationOutput := examples.DelegationOutputStorageScore()
	delegationScore := delegationOutput.StorageScore(api.StorageScoreStructure(), nil)
	printStorageScoreTestVector("Delegation Output", delegationOutput, delegationScore)
}

func storageScoreBasic() {
	basicOutput := examples.BasicOutputStorageScore()
	basicScore := basicOutput.StorageScore(api.StorageScoreStructure(), nil)
	printStorageScoreTestVector("Basic Output", basicOutput, basicScore)
}

func storageScoreAccount() {
	accountOutput := examples.AccountOutputStorageScore()
	accountScore := accountOutput.StorageScore(api.StorageScoreStructure(), nil)
	printStorageScoreTestVector("Account Output", accountOutput, accountScore)
}

func storageScoreNFT() {
	nftOutput := examples.NFTOutputStorageScore()
	nftScore := nftOutput.StorageScore(api.StorageScoreStructure(), nil)
	printStorageScoreTestVector("NFT Output", nftOutput, nftScore)
}

func storageScoreFoundry() {
	foundryOutput := examples.FoundryOutputStorageScore()
	foundryScore := foundryOutput.StorageScore(api.StorageScoreStructure(), nil)
	printStorageScoreTestVector("Foundry Output", foundryOutput, foundryScore)
}

func storageScoreAnchor() {
	anchorOutput := examples.AnchorOutputStorageScore()
	anchorScore := anchorOutput.StorageScore(api.StorageScoreStructure(), nil)
	printStorageScoreTestVector("Anchor Output", anchorOutput, anchorScore)
}

func printAddress(name string, info string, addr iotago.Address) {
	binaryLength := len(lo.PanicOnErr(api.Encode(addr)))
	hex := hexify(addr)
	bech32 := addr.Bech32(iotago.PrefixMainnet)

	fmt.Printf("- **%s (%s)**\n", name, info)
	fmt.Printf("  - Hex-encoded binary serialization (%d bytes): `%s`\n", binaryLength, hex)
	fmt.Printf("  - Bech32 string: `%s`\n", bech32)
}

func prettier(jsonBytes []byte) string {
	var out bytes.Buffer
	json.Indent(&out, jsonBytes, "", "  ")

	return out.String()
}

func jsonify(obj any) string {
	return prettier(lo.PanicOnErr(api.JSONEncode(obj, serix.WithValidation())))
}

func hexify(obj any) string {
	return hexutil.EncodeHex(lo.PanicOnErr(api.Encode(obj, serix.WithValidation())))
}

func printJson(name string, obj any) {
	fmt.Printf("%s (json-encoded):\n\n```json\n%s\n```\n\n", name, jsonify(obj))
}

func printYaml(name string, obj any) {
	reader := strings.NewReader(jsonify(obj))
	var yamlBytes strings.Builder
	json2yaml.Convert(&yamlBytes, reader)

	fmt.Printf("%s (yaml-encoded):\n\n```yaml\n%s\n```\n\n", name, yamlBytes.String())
}

func printBinary(name string, obj any) {
	fmt.Printf("%s (hex-encoded binary serialization):\n\n```\n%s\n```\n\n", name, hexify(obj))
}

func printIdentifierAndWorkScoreTestVector(name string, obj any, id string, printWorkScore bool) {
	if isYaml {
		printYaml(name, obj)
	}

	printJson(name, obj)
	printBinary(name, obj)
	fmt.Printf("%s ID:\n\n```\n%s\n```\n", name, id)

	if printWorkScore {
		workScore := lo.PanicOnErr(obj.(*iotago.Block).WorkScore())
		fmt.Printf("\n%s Work Score: `%d`.\n", name, workScore)
	}

}

func printStorageScoreTestVector(name string, obj any, storageScore iotago.StorageScore) {
	printJson(name, obj)
	printBinary(name, obj)
	fmt.Printf("%s Storage Score: `%d`.\n", name, storageScore)
}
