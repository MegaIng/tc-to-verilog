module TC_DualLoadRam (clk, rst, load0, save, address0, in, load1, address1, out0, out1);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 65536;
    parameter HEX_FILE = "test_jumps.mem";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input load0;
    input save;
    input [15:0] address0;
    input [BIT_WIDTH-1:0] in;
    input load1;
    input [15:0] address1;
    output tri0 [BIT_WIDTH-1:0] out0;
    output tri0 [BIT_WIDTH-1:0] out1;

    reg [BIT_WIDTH-1:0] outval0;
    reg [BIT_WIDTH-1:0] outval1;
    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];

    //initial begin
    //    hexfile <= HEX_FILE;
    //    if ($value$plusargs("HEXFILE=%s", hexfile)) begin
    //        $display("loading %0s", hexfile);
    //        $readmemh(hexfile, mem);
    //    end
    //end

    always @ (posedge clk or rst) begin
        if (load0 && !rst)
            outval0 <= mem[address0];
        else
            outval0 <= {BIT_WIDTH{1'bZ}};
        if (load1 && !rst)
            outval1 <= mem[address1];
        else
            outval1 <= {BIT_WIDTH{1'BZ}};
    end

    always @ (negedge clk or rst) begin
        if (save)
            mem[address0] <= in;
    end

    assign out0 = outval0;
    assign out1 = outval1;
endmodule
