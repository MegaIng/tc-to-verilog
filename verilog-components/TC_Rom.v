module TC_Rom (clk, rst, load, save, address, in, out);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 65536;
    parameter HEX_FILE = "test_jumps.mem";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in;
    output tri0 [BIT_WIDTH-1:0] out;

    reg [BIT_WIDTH-1:0] outval;
    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];

    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs("HEXFILE=%s", hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end
    end

    always @ (posedge clk) begin
        if (load)
            outval <= mem[address];
        else
            outval <= {BIT_WIDTH{1'bZ}};
    end

    always @ (negedge clk or rst) begin
        if (rst)
            mem[address] <= {BIT_WIDTH{1'b0}};
        else if (save)
            mem[address] <= in;
    end

    assign out = outval;
endmodule
