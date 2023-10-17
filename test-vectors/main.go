package main

import (
	"bytes"
	"crypto/ed25519"
	"encoding/json"
	"fmt"
	"os"
	"time"

	hiveEd25519 "github.com/iotaledger/hive.go/crypto/ed25519"
	"github.com/iotaledger/hive.go/lo"
	iotago "github.com/iotaledger/iota.go/v4"
	"github.com/iotaledger/iota.go/v4/builder"
	"github.com/iotaledger/iota.go/v4/hexutil"
	"github.com/iotaledger/iota.go/v4/tpkg"
)

const (
	// TestTokenSupply is a test token supply constant.
	TestTokenSupply        = 2_779_530_283_277_761
	ProtocolParameters     = "Protocol Parameters"
	Commitment             = "Commitment"
	Transaction            = "Transaction"
	TransactionBasicBlock  = "Transaction Basic Block"
	TaggedDataBasicBlock   = "TaggedData Basic Block"
	ValidationBlock        = "Validation Block"
	TestVectorMultiAddress = "Multi Address"
)

var (
	genesisTimestamp = time.Unix(1695275822, 0) // 2023-09-21 13:57:02 +0800 CST
	api              = iotago.V3API(
		iotago.NewV3ProtocolParameters(
			iotago.WithNetworkOptions("TestJungle", "tgl"),
			iotago.WithTimeProviderOptions(genesisTimestamp.Unix(), 10, 13),
			iotago.WithManaOptions(63, 1, 17, []uint32{10, 20}, 32, 2420916375, 21),
			iotago.WithSupplyOptions(TestTokenSupply, 0, 0, 0, 0, 0, 0),
			iotago.WithWorkScoreOptions(0, 1, 0, 0, 0, 0, 0, 0, 0, 0), // all zero except block offset gives all blocks workscore = 1
		),
	)
	supportedObjects = []string{
		ProtocolParameters,
		Commitment,
		Transaction,
		TransactionBasicBlock,
		TaggedDataBasicBlock,
		ValidationBlock,
		TestVectorMultiAddress,
	}
)

func main() {
	if len(os.Args) <= 1 {
		return
	}
	name := os.Args[1]

	switch name {
	case ProtocolParameters:
		protocolParameters()
	case Commitment:
		commitmentExample()
	case Transaction:
		txExample()
	case TransactionBasicBlock:
		basicBlockTxExample()
	case TaggedDataBasicBlock:
		basicBlockTaggedDataExample()
	case ValidationBlock:
		validationBlockExample()
	case TestVectorMultiAddress:
		multiAddressTestVector()
	default:
		fmt.Println("Usage: go run main.go \"[object name]\"")
		fmt.Println("Supported object:")
		for _, o := range supportedObjects {
			fmt.Println("\t -", o)
		}
	}
}

func protocolParameters() {
	jp, _ := api.JSONEncode(api.ProtocolParameters())
	fmt.Printf("%s\n", prettier(jp))

	b, _ := api.Encode(api.ProtocolParameters())
	fmt.Println(b)
	fmt.Printf("\nProtocol Parameters Hash: %s\n\n", lo.Return1(api.ProtocolParameters().Hash()).ToHex())
}

func commitmentExample() {
	commitment := iotago.Commitment{
		ProtocolVersion:      api.Version(),
		Slot:                 18,
		PreviousCommitmentID: tpkg.RandCommitmentInput().CommitmentID,
		RootsID:              tpkg.RandCommitmentInput().CommitmentID.Identifier(),
		CumulativeWeight:     89,
		ReferenceManaCost:    144,
	}

	printIdentifierTestVector("Slot Commitment", commitment, commitment.MustID().ToHex())
}

func txExample() {
	keyPair := hiveEd25519.GenerateKeyPair()
	addr := iotago.Ed25519AddressFromPubKey(keyPair.PublicKey[:])

	output1 := &iotago.BasicOutput{
		Amount: 100000,
		Conditions: iotago.BasicOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.BasicOutputFeatures{
			tpkg.RandNativeTokenFeature(),
		},
	}

	output2 := &iotago.AccountOutput{
		Amount: 100000,
		Mana:   5000,
		Conditions: iotago.AccountOutputUnlockConditions{
			&iotago.StateControllerAddressUnlockCondition{
				Address: addr,
			},
			&iotago.GovernorAddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.AccountOutputFeatures{
			&iotago.MetadataFeature{
				Data: tpkg.RandBytes(16),
			},
		},
	}

	creationSlot := iotago.SlotIndex(1 << 20)
	tx := lo.PanicOnErr(builder.NewTransactionBuilder(api).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      tpkg.RandOutputID(0),
			Input:        output1,
		}).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      tpkg.RandOutputID(0),
			Input:        output2,
		}).
		AddOutput(output1).
		AddOutput(output2).
		AddContextInput(&iotago.CommitmentInput{CommitmentID: iotago.NewCommitmentID(85, tpkg.Rand32ByteArray())}).
		AddContextInput(&iotago.BlockIssuanceCreditInput{AccountID: tpkg.RandAccountID()}).
		AddContextInput(&iotago.RewardInput{Index: 0}).
		IncreaseAllotment(tpkg.RandAccountID(), tpkg.RandMana(10000)+1).
		IncreaseAllotment(tpkg.RandAccountID(), tpkg.RandMana(10000)+1).
		WithTransactionCapabilities(
			iotago.TransactionCapabilitiesBitMaskWithCapabilities(iotago.WithTransactionCanBurnNativeTokens(true)),
		).
		SetCreationSlot(creationSlot).
		Build(iotago.NewInMemoryAddressSigner(iotago.AddressKeys{Address: addr, Keys: ed25519.PrivateKey(keyPair.PrivateKey[:])})))

	printIdentifierTestVector("Transaction", tx, lo.PanicOnErr(tx.ID()).ToHex())
}

func basicBlockTxExample() {
	basicBlock := tpkg.RandBasicBlock(api, iotago.PayloadSignedTransaction)
	signedTx := tpkg.RandSignedTransactionWithTransaction(api, tpkg.RandTransactionWithOptions(
		api,
		tpkg.WithUTXOInputCount(2),
		tpkg.WithOutputCount(2),
		tpkg.WithAllotmentCount(1),
	))
	basicBlock.Payload = signedTx
	block := tpkg.RandProtocolBlock(basicBlock, api, 100)
	block.IssuingTime = genesisTimestamp.Add(12 * time.Second)

	printIdentifierTestVector("Block", block, block.MustID().ToHex())
}

func basicBlockTaggedDataExample() {
	basicBlock := tpkg.RandBasicBlock(api, iotago.PayloadTaggedData)
	block := tpkg.RandProtocolBlock(basicBlock, api, 100)
	block.IssuingTime = genesisTimestamp.Add(12 * time.Second)

	printIdentifierTestVector("Block", block, block.MustID().ToHex())
}

func validationBlockExample() {
	basicBlock := tpkg.RandValidationBlock(api)
	block := tpkg.RandProtocolBlock(basicBlock, api, 100)
	block.IssuingTime = genesisTimestamp.Add(12 * time.Second)
	block.Block.(*iotago.ValidationBlock).ProtocolParametersHash = lo.Return1(api.ProtocolParameters().Hash())

	printIdentifierTestVector("Block", block, block.MustID().ToHex())
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

func prettier(jsonBytes []byte) string {
	var out bytes.Buffer
	json.Indent(&out, jsonBytes, "", "  ")

	return out.String()
}

func jsonify(obj any) string {
	return prettier(lo.PanicOnErr(api.JSONEncode(obj)))
}

func printIdentifierTestVector(name string, obj any, id string) {
	fmt.Printf("%s (json-encoded):\n\n```json\n%s\n```\n\n", name, jsonify(obj))
	fmt.Printf("%s (binary-encoded):\n\n```\n%s\n```\n\n", name, hexify(obj))
	fmt.Printf("%s ID:\n\n```\n%s\n```\n", name, id)
}

func hexify(obj any) string {
	return hexutil.EncodeHex(lo.PanicOnErr(api.Encode(obj)))
}
