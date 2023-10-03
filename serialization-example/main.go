package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/iotaledger/hive.go/lo"
	iotago "github.com/iotaledger/iota.go/v4"
)

const (
	// TestTokenSupply is a test token supply constant.
	TestTokenSupply        = 2_779_530_283_277_761
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
			iotago.WithWorkScoreOptions(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), // all zero except block offset gives all blocks workscore = 1
		),
	)
	supportedObjects = []string{
		"Protocol Parameters",
		"Commitment",
		"Transaction",
		"Transaction Basic Block",
		"TaggedData Basic Block",
		"Validation Block",
		TestVectorMultiAddress,
	}
)

func main() {
	if len(os.Args) <= 1 {
		return
	}
	name := os.Args[1]

	switch name {
	case "Protocol Parameters":
		protocolParameters()
	case "Commitment":
		commitmentExample()
	case "Transaction":
		txExample()
	case "Transaction Basic Block":
		basicBlockTxExample()
	case "TaggedData Basic Block":
		basicBlockTaggedDataExample()
	case "Validation Block":
		validationBlockExample()
	case TestVectorMultiAddress:
		multiAddressTestVector()
	case "help", "-h", "--help", "-help":
		fmt.Println("Usage: go run main.go \"[object name]\"")
		fmt.Println("Supported object:")
		for _, o := range supportedObjects {
			fmt.Println("\t -", o)
		}
	}
}

func protocolParameters() {
	fmt.Println(">>>>>>>> ProtocolParameters >>>>>>>>")

	jp, _ := api.JSONEncode(api.ProtocolParameters())
	fmt.Printf("%s\n", prettier(jp))

	b, _ := api.Encode(api.ProtocolParameters())
	fmt.Println(b)
	fmt.Printf("\nProtocol Parameters Hash: %s\n\n", lo.Return1(api.ProtocolParameters().Hash()).ToHex())
}

func commitmentExample() {
	fmt.Println(">>>>>>>> Commitment >>>>>>>>")

	commitmentJSON := "{\"protocolVersion\":3,\"slot\":10,\"previousCommitmentId\":\"0x4b024b3e47280d05272a7d136f0c464e4e136b734e6c427749413e286162077560652c007e37241a\",\"rootsId\":\"0x75614402763f5f045c040334631b791b4d755d626d504b134a505c001c516549\",\"cumulativeWeight\":\"100\",\"referenceManaCost\":\"6000\"}"

	fmt.Println(prettier([]byte(commitmentJSON)))

	commitment := &iotago.Commitment{}
	api.JSONDecode([]byte(commitmentJSON), commitment)

	b, _ := api.Encode(commitment)
	fmt.Println(b)

	fmt.Printf("Commitment ID: %s\n\n", commitment.MustID().ToHex())
}

func txExample() {
	fmt.Println(">>>>>>>> TX >>>>>>>>")

	blockJSON := "{\"type\":6,\"essence\":{\"type\":2,\"networkId\":\"3650798313638353144\",\"creationSlot\":28,\"contextInputs\":[],\"inputs\":[{\"type\":0,\"transactionId\":\"0x010203040506070000000000000000000000000000000000000000000000000000000000\",\"transactionOutputIndex\":10}],\"inputsCommitment\":\"0xb70c6f86a1ea03a59a71d73dcd07e2082bbdf0ce971faa21748348bca22fb023\",\"outputs\":[{\"type\":3,\"amount\":\"10000\",\"mana\":\"0\",\"unlockConditions\":[{\"type\":0,\"address\":{\"type\":0,\"pubKeyHash\":\"0xd9f84458286dc41cd34789dec566cd096cf47de991aa36a97aebfaea14128f6d\"}}]}],\"allotments\":[],\"payload\":{\"type\":5,\"tag\":\"0x1d7b3e11697264111e130b0e\",\"data\":\"0x1d7b3e11697264111e130b0e\"}},\"unlocks\":[{\"type\":0,\"signature\":{\"type\":0,\"publicKey\":\"0x803361fe1effc899dca7f931d8ad07c01ba23aaa93f986adb04d4c17cf6368d8\",\"signature\":\"0xccddbac3aaac413e0193e16da3449f30c183d0e7eaa7f303dc12ae0dbc9fb890e449a52f9056e7d952ea796fd3e5645f60d9eb98ed91cb3261720fb528d2a105\"}}]}"

	fmt.Println(prettier([]byte(blockJSON)))

	tx := &iotago.Transaction{}
	api.JSONDecode([]byte(blockJSON), tx)

	b, _ := api.Encode(tx)
	fmt.Println(b)

	fmt.Printf("TXID: %s\n\n", lo.Return1(tx.ID()).ToHex())
}

func basicBlockTxExample() {
	fmt.Println(">>>>>>>> BasicBlock - TX >>>>>>>>")

	blockJSON := "{\"protocolVersion\":3,\"networkId\":\"10549460113735494767\",\"issuingTime\":\"1675563954966263210\",\"slotCommitmentId\":\"0x498bf08a5ed287bc87340341ffab28706768cd3a7035ae5e33932d9a12bb30940000000000000000\",\"latestFinalizedSlot\":21,\"issuerId\":\"0x3370746f30705b7d0b42597459714d45241e5a64761b09627c447b751c7e145c\",\"block\":{\"type\":0,\"strongParents\":[\"0x304442486c7a05361408585e4b5f7a67441c437528755a70041e0e557a6d4b2d7d4362083d492b57\",\"0x5f736978340a243d381b343b160b316a6b7d4b1e3c0355492e2e72113c2b126600157e69113c0b5c\"],\"weakParents\":[\"0x0b5a48384f382f4a49471c4860683c6f0a0d446f012e1b117c4e405f5e24497c72691f43535c0b42\"],\"shallowLikeParents\":[\"0x163007217803006078040b0f51507d3572355a457839095e572f125500401b7d220c772b56165a12\"],\"payload\":{\"type\":6,\"essence\":{\"type\":2,\"networkId\":\"3650798313638353144\",\"creationSlot\":28,\"contextInputs\":[],\"inputs\":[{\"type\":0,\"transactionId\":\"0x010203040506070000000000000000000000000000000000000000000000000000000000\",\"transactionOutputIndex\":10}],\"inputsCommitment\":\"0xb70c6f86a1ea03a59a71d73dcd07e2082bbdf0ce971faa21748348bca22fb023\",\"outputs\":[{\"type\":3,\"amount\":\"10000\",\"mana\":\"0\",\"unlockConditions\":[{\"type\":0,\"address\":{\"type\":0,\"pubKeyHash\":\"0xd9f84458286dc41cd34789dec566cd096cf47de991aa36a97aebfaea14128f6d\"}}]}],\"allotments\":[],\"payload\":{\"type\":5,\"tag\":\"0x1d7b3e11697264111e130b0e\",\"data\":\"0x1d7b3e11697264111e130b0e\"}},\"unlocks\":[{\"type\":0,\"signature\":{\"type\":0,\"publicKey\":\"0x803361fe1effc899dca7f931d8ad07c01ba23aaa93f986adb04d4c17cf6368d8\",\"signature\":\"0xccddbac3aaac413e0193e16da3449f30c183d0e7eaa7f303dc12ae0dbc9fb890e449a52f9056e7d952ea796fd3e5645f60d9eb98ed91cb3261720fb528d2a105\"}}]},\"burnedMana\":\"180500\"},\"signature\":{\"type\":0,\"publicKey\":\"0x024b6f086177156350111d5e56227242034e596b7e3d0901180873740723193c\",\"signature\":\"0x7c274e5e771d5d60202d334f06773d3672484b1e4e6f03231b4e69305329267a4834374b0f2e0d5c6c2f7779620f4f534c773b1679400c52303d1f23121a4049\"}}"

	basicBlock := &iotago.ProtocolBlock{}
	api.JSONDecode([]byte(blockJSON), basicBlock)

	basicBlock.IssuingTime = genesisTimestamp.Add(12 * time.Second)
	b, _ := api.JSONEncode(basicBlock)
	fmt.Println(prettier(b))

	b, _ = api.Encode(basicBlock)
	fmt.Println(b)

	fmt.Printf("BlockID: %s %d\n\n", basicBlock.MustID().ToHex(), basicBlock.MustID().Index())
}

func basicBlockTaggedDataExample() {
	fmt.Println(">>>>>>>> BasicBlock - TaggedData >>>>>>>>")

	blockJSON := "{\"protocolVersion\":3,\"networkId\":\"10549460113735494767\",\"issuingTime\":\"1675563954966263210\",\"slotCommitmentId\":\"0x498bf08a5ed287bc87340341ffab28706768cd3a7035ae5e33932d9a12bb30940000000000000000\",\"latestFinalizedSlot\":21,\"issuerId\":\"0x3370746f30705b7d0b42597459714d45241e5a64761b09627c447b751c7e145c\",\"block\":{\"type\":0,\"strongParents\":[\"0x304442486c7a05361408585e4b5f7a67441c437528755a70041e0e557a6d4b2d7d4362083d492b57\",\"0x5f736978340a243d381b343b160b316a6b7d4b1e3c0355492e2e72113c2b126600157e69113c0b5c\"],\"weakParents\":[\"0x0b5a48384f382f4a49471c4860683c6f0a0d446f012e1b117c4e405f5e24497c72691f43535c0b42\"],\"shallowLikeParents\":[\"0x163007217803006078040b0f51507d3572355a457839095e572f125500401b7d220c772b56165a12\"],\"payload\":{\"type\":5,\"tag\":\"0x68656c6c6f20776f726c64\",\"data\":\"0x01020304\"},\"burnedMana\":\"180500\"},\"signature\":{\"type\":0,\"publicKey\":\"0x024b6f086177156350111d5e56227242034e596b7e3d0901180873740723193c\",\"signature\":\"0x7c274e5e771d5d60202d334f06773d3672484b1e4e6f03231b4e69305329267a4834374b0f2e0d5c6c2f7779620f4f534c773b1679400c52303d1f23121a4049\"}}"

	basicBlock := &iotago.ProtocolBlock{}
	api.JSONDecode([]byte(blockJSON), basicBlock)

	basicBlock.IssuingTime = genesisTimestamp.Add(12 * time.Second)
	b, _ := api.JSONEncode(basicBlock)
	fmt.Println(prettier(b))

	b, _ = api.Encode(basicBlock)
	fmt.Println(b)

	fmt.Printf("BlockID: %s %d\n\n", basicBlock.MustID().ToHex(), basicBlock.MustID().Index())
}

func validationBlockExample() {
	fmt.Println(">>>>>>>> ValidationBlock >>>>>>>>")

	blockJSON := "{\"protocolVersion\":3,\"networkId\":\"10549460113735494767\",\"issuingTime\":\"1675563954966263210\",\"slotCommitmentId\":\"0x498bf08a5ed287bc87340341ffab28706768cd3a7035ae5e33932d9a12bb30940000000000000000\",\"latestFinalizedSlot\":0,\"issuerId\":\"0x3370746f30705b7d0b42597459714d45241e5a64761b09627c447b751c7e145c\",\"block\":{\"type\":1,\"strongParents\":[\"0x304442486c7a05361408585e4b5f7a67441c437528755a70041e0e557a6d4b2d7d4362083d492b57\",\"0x5f736978340a243d381b343b160b316a6b7d4b1e3c0355492e2e72113c2b126600157e69113c0b5c\"],\"weakParents\":[\"0x0b5a48384f382f4a49471c4860683c6f0a0d446f012e1b117c4e405f5e24497c72691f43535c0b42\"],\"shallowLikeParents\":[\"0x163007217803006078040b0f51507d3572355a457839095e572f125500401b7d220c772b56165a12\"],\"highestSupportedVersion\":3,\"protocolParametersHash\":\"0x0000000000000000000000000000000000000000000000000000000000000000\"},\"signature\":{\"type\":0,\"publicKey\":\"0x024b6f086177156350111d5e56227242034e596b7e3d0901180873740723193c\",\"signature\":\"0x7c274e5e771d5d60202d334f06773d3672484b1e4e6f03231b4e69305329267a4834374b0f2e0d5c6c2f7779620f4f534c773b1679400c52303d1f23121a4049\"}}"

	validationBlock := &iotago.ProtocolBlock{}
	api.JSONDecode([]byte(blockJSON), validationBlock)
	validationBlock.Block.(*iotago.ValidationBlock).ProtocolParametersHash = lo.Return1(api.ProtocolParameters().Hash())

	validationBlock.IssuingTime = genesisTimestamp.Add(12 * time.Second)

	jb, _ := api.JSONEncode(validationBlock)
	fmt.Printf("%s\n\n", prettier(jb))

	b, _ := api.Encode(validationBlock)
	fmt.Println(b)

	fmt.Printf("BlockID: %s %d\n\n", validationBlock.MustID().ToHex(), validationBlock.MustID().Index())
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

	json := lo.PanicOnErr(api.JSONEncode(addr))

	fmt.Printf("%s\n\n", prettier(json))

	fmt.Printf("%s\n\n", addrRef.Bech32(iotago.PrefixMainnet))
}

func prettier(jsonBytes []byte) string {
	var out bytes.Buffer
	json.Indent(&out, jsonBytes, "", "  ")

	return out.String()
}
